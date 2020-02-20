#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

__author__ = "Jeffrey Mvutu Mabilama (jeffrey.mvutu@gmail.com)"
__version__ = "0.1.0.0.0.1"
__copyright__ = "Copyright (c) 2017-2019 Jeffrey Mvutu Mabilama"
__license__ = "All rights reserved"


import os
import datetime

import pytest

# import jmm.configurations as script
# import jmm.configurations as script  # this would use the installed version of the package for testing instead of the development one.
from .. import configurations as script

## Monkeypatching with pytest
# https://docs.pytest.org/en/latest/monkeypatch.html


def test_get_user_custom_settings_folder_from_user_root(monkeypatch):
	make_lamdbas = lambda *values: [(lambda : val) for i, val in enumerate(values)]
	make_patches = lambda member_names, funcs: [monkeypatch.setattr(script, name, fn, raising=True) for name, fn in zip(member_names, funcs)]
	
	def mock_expanduser(path):
		if path[0] == "~":
			path = "/Users/foo_user" + path[1:]
		return path
	
	### Unix test
	if os.sys.platform.lower() in ['linux', 'linux2', 'darwin']:
		monkeypatch.setattr(os.path, "expanduser", mock_expanduser)
		
		rvals = make_lamdbas(False, True, False)
		make_patches(["is_windows", "is_macos", "is_linux"], rvals)
		assert "/Users/foo_user/.settings" == os.path.abspath(script.get_user_custom_settings_folder_from_user_root())
		assert "/Users/foo_user/.settings/my_app" == os.path.abspath(script.get_user_custom_settings_folder_from_user_root("my_app"))
	else:
		# Until we can create a working test for Windows, we consider
		# the function may not work properly, hence the test should fail.
		assert False
	pass
