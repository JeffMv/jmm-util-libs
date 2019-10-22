#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module that informs about the system configuration
And provides some support utils that are NOT intended to be cross-platform.

Further work would be needed to make this module working with other OSes.

The module was first developped with MacOS in mind.
"""

import os
import platform
import shutil


############## Systems and OS #################

# a preferences manager

def get_user_custom_settings_folder_from_user_root(subpath=None):
    """Creates a folder in the root folder of the current user [not meant to
    support root/super users without a personal user directory] if not existing
    and returns its path.
    
    You may prefer using a folder outside of the usual preferences' location
    of sandboxed apps (in MacOS: ~/Library/Preferences) if your script is not
    a real application, especially in experimentation stages.
    You might not want to 'pollute' such an official
    directory and prefer this one instead, where you can simply create a
    subfolder for your app's settings and remove them whenever you want to
    reset the settings for instance.
    
    Inspired from https://stackoverflow.com/a/10644400/4418092
    
    :returns: the path to the folder, or None the folder is unavailable
        (permission error for instance). Note that some permissions (like maybe
        no reading + no writing) may
        interfere with this function and create weird results.
        Though, simple permissions that only prevent writing while allowing
        reading should not cause issues.
    """
    user_path = os.path.expanduser('~')
    if is_windows():
        # On Windows, it can contain double drive prefix like 'C:C:\Users\myuser'
        # see this question https://stackoverflow.com/questions/34560209/pythons-os-path-expanduser-schizophrenic-windows-behaviour/34560323
        drive_prefix = user_path[:2]
        user_path = user_path[2:] if user_path[:4].count(drive_prefix) > 1 else user_path
    
    directory = os.path.join(user_path, '.settings')
    directory = os.path.join(directory, subpath) if subpath is not None else directory
    try:
        # os.makedirs(directory, exist_ok=True) # no side effect. this function is a query
        pass
    except FileExistsError:
        pass
    except PermissionError:
        directory = None
    return directory


### Identifying the major OS type

def is_windows():
    """Tells whether the current OS is Windows"""
    return os.sys.platform.lower() in ['win32', 'win64']

def is_macos():
    """Tells whether the current OS is MacOS"""
    return os.sys.platform.lower() in ['darwin']

def is_linux():
    """Tells whether the current OS is Linux"""
    return os.sys.platform.lower() in ['linux', 'linux2']


# Determining the OS
# https://stackoverflow.com/questions/1854/python-what-os-am-i-running-on

def get_os_indentification_info():
    _platform = os.sys.platform
    is_win, is_mac, is_linux = [False] * 3
    if _platform == "linux" or _platform == "linux2":
        # linux
        is_linux = True
    elif _platform == "darwin":
        # MAC OS X
        is_mac = True
    elif _platform == "win32":
        # Windows
        is_win = True
    elif _platform == "win64":
        # Windows 64-bit
        is_win = True
    return is_linux, is_win, is_mac


## Getting the battery level on MacOS from a shell call to os.system("pmset -g batt")
# import subprocess
# tmp = subprocess.run(["pmset", "-g", "batt"], stdout=subprocess.PIPE) if is_macos() else None
# tmp.stdout.decode() if tmp is not None else None


############## Filesystem : OS-specific #################


def get_volumes_with_free_space(lower_bound, upper_bound=None):
    """Returns a list of mounted disks that have the specified amount of free space.
    :param lower_bound: the minimum number of free bytes you expect.
    :param upper_bound: the maximum number of free bytes you expect.
    :note: Only available on systems where mounted volumes are in /Volumes
    """
    root, disks, _ = next(os.walk("/Volumes"))
    drives = []
    disk_spaces = []
    for hd in disks:
        disk_path = os.path.join(root, hd)
        free_bytes = shutil.disk_usage(disk_path).free
        satisfies_lower = (lower_bound is None) or (lower_bound <= free_bytes)
        satisfies_upper = (upper_bound is None) or (free_bytes <= upper_bound)
        if satisfies_lower and satisfies_upper:
            drives.append(disk_path)
            disk_spaces.append(free_bytes)
    return drives, disk_spaces
