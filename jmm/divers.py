#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

import os
import sys
import string
import random
import base64
import calendar

from datetime import date, datetime
from threading import Thread
from urllib.parse import (unquote, quote)



################### Utils ####################


def overrides(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider


def padSymbols(s, width, symbol="0", to_front=True):
    """
    :warning: Warning, the function does not behave the same with floating points, depending on the version of Python
    """
    s = str(s)
    symbol = str(symbol)
    #
    count = int(width) - len(s)
    count = count if count > 0 else 0
    queue = count * symbol
    res = (queue + s) if to_front else (s + queue)
    return res


def padZerosToNumber(n, nZeros):
    """
    :warning: Warning, the function does not behave the same with floating points, depending on the version of Python
    """
    version = sys.version[:3]
    if version >= "3.6":
        return f'{n:0{nZeros}}'
    # elif "3.0" <= version and version <= "3.5":
    #     return '{0:0dd}'.format(nZeros, n)
    elif version <= "2.9":
        # This foes not output floats (only integers)
        return "%0{}.f".format(nZeros) % 10
    else:
        print("Error. You might want to use the function padSymbols instead and pass it a string.")
        raise NameError("Unsupported padding operation. Please update the code")
        # return padSymbols(n, nZeros, '0', True)


def stripExtra(text, pattern, keep=1):
    """Strips patterns within a string.
    :param str text: the text to process
    :param str pattern: pattern or pattern to replace
    :param int keep: how many of the
    
    >>> text = '   hello... how are youuuu   ?  '
    >>> text = stripExtra(text, '...', 1)  # this will not change text
    >>> text = stripExtra(text, 'u', 1)  # this will change 'youuuu' to 'you'
    """
    pattern_of_extra = pattern * (keep + 1)
    replace_with = pattern * keep
    previous_size = len(text)
    can_shrink = True
    while can_shrink:
        text = text.replace(pattern_of_extra, replace_with)
        can_shrink = len(text) < previous_size
        previous_size = len(text)
    return text


################### Files, folders and encoding ####################

def ls(path="."):
    """
    Alias for next(os.walk(path))
    """
    res = next(os.walk(path))
    return res

def pickle_dumps(pickleShelf, **kwargs):
    """
    """
    for key in kwargs:
        pickleShelf[key] = kwargs[key]


def pickle_loads(pickleShelf, localsDict):
    """Load variables from an opened shelf into a <dict> dictionary
    :param: localsDict: the result of locals(). For scope reasons, you must pass it yourself
    
    :note: if the function does not update your local variables, you can do the following:
        tmp = pickleLoads(shelf, locals());
        [locals().update( {key: tmp[key]} ) for key in tmp]
    """
    for key in pickleShelf:
        localsDict[key] = pickleShelf[key]
    return localsDict


def replace_file_extension(path, extension):
    """replaces the file extension (and add one if there is no current extension).
    """
    path = ".".join(path.split('.')[:-1] + [extension])
    return path


def append_to_basename(path, name):
    path = path[:-1] if path.endswith(os.path.sep) else path
    directory = os.path.dirname(path)
    last_part = os.path.basename(path)
    
    parts = last_part.split('.')
    if len(parts) == 1:
        # last_part might be a directory / file without extension
        ext = None
        base = last_part  # here: parts[0] == last_part
    elif len(parts) == 2 and parts[0] == '':
        # for cases like last_part = ".base-alone"
        ext = None
        base = last_part
    elif last_part.find('..') == 0 and last_part.find(os.path.join('..', '')) < 0:
        # for cases like path = "path/to/..something"
        raise ValueError("Inconsistent basename")
    else:
        ext = parts[-1]
        base = '.'.join(parts[:-1])
    
    base = base + name
    filename = base + (("." + ext) if ext else '')
    return os.path.join(directory, filename)


def get_file_size(filepath):
    """Returns the file size of a specified file in bytes.
    :param filepath:
    :throw: FileNotFoundError if file does not exist
    """
    size = os.path.getsize(filepath)
    # or
    # size = os.stat(filepath).st_size
    return size


def url_decode(s):
    return unquote(s)


def url_encode(s):
    return quote(s)


def base64_decode(s, silence_errors=True, encoding='utf-8'):
    """
    src: https://stackoverflow.com/questions/3470546/python-base64-data-decode
    
    :param silence_errors: whether you want basic errors to be handled or not.
            If False, will throw `binascii.Error` if the string is already
            decoded, but with True, it will return the original string.
    """
    if silence_errors:
        try:
            return base64.b64decode(s).decode(encoding)
        except base64.binascii.Error:
            return s
    else:
        return base64.b64decode(s).decode(encoding)


def base64_encode(b):
    """Url encodes the bytes"""
    return base64.b64encode(b)


def insertInFile(s, file, index):
    """Inserts text in a file at the specified index.
    :note: it does *read the whole file* and inserts at the given position,
            so be wary of really big files.
    :param str s: the string to insert
    :param str or filehandle file: the filepath or filehandle you want to insert to
    :param int index: the position to insert to. 0 means at start of file.
    """
    file = open(file, 'r') if isinstance(file, str) else file;
    filename = file.name;
    fc = file.read(); file.close()
    # Insert the new content
    newContent = fc[:index] + s + fc[index:]
    file = open(filename, 'w')
    file.write(newContent)
    file.close() #save


################### Dates and times ####################


hourAsString = lambda d: padZerosToNumber(d.hour,2) + "h" + padZerosToNumber(d.minute, 2)


def hourFromString(s):
    """
    Convertit une heure texte en tuple
    Les caractères acceptés pour l'affichage de l'heure: 15h30, 15:30
    """
    if s is None or not isinstance(s, str):
        raise ValueError("Expected <str>")
    
    s = s.strip()
    hasHour = (s is not None) and len(s)==5 and ['h',':'].count(s[2]) > 0  # regarde le caractère au milieu: 15h30, 15:30
    try:
        theHour = (int(s[:2]) , int(s[3:])) if hasHour else None
    except ValueError:
        theHour = None
        raise ValueError("Cannot read hour format")
    return theHour


def getDateAsStr(d):
    """
    [date object] -> 'yyyy-mm-dd'
    """
    day = str(d.day) if d.day >= 10 else '0'+str(d.day)
    month = str(d.month) if d.month >= 10 else '0'+str(d.month)
    year = str(d.year)
    return  year +'-'+ month +'-'+ day


def dateFormattedAsYMA(aDate, sep='-'):
    """
    datetime.date -> 'yyyy-mm-dd'
    """
    res = "%i-%s-%s" % (aDate.year, padZerosToNumber(aDate.month,2), padZerosToNumber(aDate.day,2))
    res = sep.join(res.split('-'))
    return res


def weekday_number(aDate):
    """Retourne l'index du jour de la semaine où tombe la date spécifiée"""
    return calendar.weekday(aDate.year, aDate.month, aDate.day)


def dateToDatetime(d):
    """
    Retourne un objet datetime.datetime à partir d'un objet datetime.date
    """
    return datetime(d.year, d.month, d.day, 0, 0, 0)


def datetimeToDate(d):
    """
    Retourne un objet datetime.date à partir d'un objet datetime.datetime
    """
    return date(d.year, d.month, d.day)


# def dateFromComponents(components, compOrder, sep='-'):
#     """
#     Retourne un objet datetime.date à partir de composantes
#     :note: example 
#     """
#     if isinstance(components, str):
#         if len(components)>0:
#             components = splitToInts(components, sep)
#     elif len(components)>0 and isinstance(components[0], str):
#         components = [int(c) for c in components]


################### Stats ####################

def frequences(arr, returnSplitted=True, hashAsString=False, U=None, frequenciesOverUniverse=None):
    """
    """
    if U is None:
        return effectif(arr, returnSplitted, hashAsString, True)
    else:
        return effectifU(arr, U, returnSplitted, hashAsString, True, frequenciesOverUniverse)
    

def effectif(arr, returnSplitted=False, hashAsString=False, frequencies=False, inputConverter=None, sort=False, reverse=False):
    """calcule l'effectif
    :param list arr: une liste
    :param bool hashAsString: whether we should convert the values in 'arr' to
                string before comparing them
    :param function inputConverter: a callable function that is used to convert
                the values within arr into the class you want the values to be
                compared as. When not provided, the identity function is used.
                If used with parameter 'hashAsString', the hashed value will be
                the one returned by this function.
    :param bool sort: sort the result (only if returnSplitted). Shorthand for `sortBasedOn`
    :param bool reverse: reverse the order (only if sort and returnSplitted). Shorthand for `sortBasedOn`
    """
    inputConverter = (lambda x: x) if inputConverter is None else inputConverter
    effs = {}
    for val in arr:
        val = inputConverter(val)
        key = str(val) if hashAsString else val
        try:
            effs[key] = effs[key]+1
        except:
            effs[key] = 1
    
    if frequencies:
        tot = sum(effs.values())
        for key in effs:
            effs[key] = effs[key]/tot
    
    if returnSplitted:
        xis = list(effs.keys())
        nis = list(effs.values())
        if sort:
            xis, nis = sortBasedOn(nis, xis, nis, reverse=reverse)
        return xis, nis
    
    return effs


def effectif_u(arr, U=None, returnSplitted=False, hashAsString=False, frequencies=False, frequenciesOverUniverse=True, inputConverter=None):
    """calcule l'effectif
    :param arr: une liste
    :param U: (univers) liste des valeurs possibles
    """
    # if hashAsString:
    #     raise Exception("unsupported")
    
    inputConverter = (lambda x: x) if inputConverter is None else inputConverter
    
    U = U if not (U is None) else Octave.unique(arr)
    U = [inputConverter(v) for v in U]
    
    effs = {}
    for u in U:
        u = str(u) if hashAsString else u
        effs[u] = 0
    
    for val in arr:
        val = inputConverter(val)
        val = str(val) if hashAsString else val
        try:
            effs[val] = effs[val]+1
        except:
            pass  # do not count values that are not in the given universe
    
    if frequencies:
        tot = sum(effs.values()) if frequenciesOverUniverse else len(arr)
        for key in effs:
            effs[key] = effs[key]/tot
    
    if returnSplitted:
        xis = list(effs.keys())
        nis = list(effs.values())
        return xis, nis
    
    return effs





######## Data structures manipulation #########


def split_evenly_in_increasing_order(arr, nbGroups):
    """Splits an array evenly and returns the result.
    :param list arr:
    :param int nbGroups:
    :return: list<list<>>
    >>> split_evenly_in_increasing_order(list(range(20, 31), 3))
    [[20, 23, 26, 29], [21, 24, 27,30], [22, 25, 28]]
    """
    remainder = len(arr) % nbGroups
    upto = len(arr) - remainder
    groupLength = (len(arr) - remainder) // nbGroups
    
    result = [[] for _ in range(nbGroups)]
    indexGroups = []
    for groupIndex in range(nbGroups):
        targetGroupIndexes = range(0 + groupIndex, len(arr), nbGroups)
        indexGroups.append(list(targetGroupIndexes))
        for mainArrIndex in targetGroupIndexes:
            value = arr[mainArrIndex]
            result[groupIndex].append(value)
    
    return result


def flatten_iterable(array):
    """
    :param iter<T> array:
    """
    res = []
    for el in array:
        try:
            res += list(el)
        except:
            res += [el]
    return res

def flatten_list(array):
    return flatten_iterable(array)

def concatenate_sublists(array):
    """
    like `flatten_iterable`, but raises 
    :param list<list> array:
    """
    res = []
    for arr in array:
        try:
            res += arr
        except TypeError:
            raise TypeError("Only supports list objects at the second level.")
    return res


def fill_empty_dict_entries(adict, *other_dicts):
    """Merge dictionary values into the specified one, replacing only
    None values.
    """
    # :param func rule:
    empty_entries = [key for key in adict if adict[key] is None]
    for key in empty_entries:
        i = 0
        while adict[key] is None and i < len(other_dicts):
            other = other_dicts[i]
            if other.get(key) is not None:
                adict[key] = other[key]
            i += 1
    return adict, empty_entries


def flatten_json(collection, delim):
    return (flatten_dict(collection, delim))

def flatten_dict(collection, delim, custom_key_mgr=None):
    """Flattens a dictionary by recursively appending the paths to the end nodes.
    :param collection: 
    :param str delim: the delimiter to join the paths with
    :param func custom_key_mgr: A function that converts *ALL* dict keys to
                an str type equivalent. Default is `str()`.
                It's main use is to convert  non-JSON compatible Python dict like
                `{"1": "string key", 1: "int key"}`.
    :source: https://stackoverflow.com/a/28246154/4418092
    
    :note: Python allows similar keys to be defined inside `dict`s without complaining
            but JSON does not. Hence, the dict {"1": "string key", 1: "int key"} is valid
            in Python but not in JSON.
            Moreover, due to the way the dict is flattened, such cases could override values.
            You should then provide a function to specify how to handle custom types of keys.
            The order of parsing is not given.
    
    >>> dictionary = {"a": {"subA": "hello", "myarray": ["Hi", "dear"]}, "b": 12, 49: {"hello": "world"}}
    >>> flatten_dict(dictionary, "__")
    {
        'a__subA': 'hello', 
        'a__myarray__0': 'Hi',
        'a__myarray__1': 'dear',
        'b': 12,
        '49__hello': 'world'
    }
    """
    custom_key_mgr = lambda value: str(value)
    val = {}
    if isinstance(collection, dict):
        for i in collection.keys():
            if isinstance( collection[i], dict ):
                subvalues = flatten_dict( collection[i], delim )
                for j in subvalues.keys():
                    val[ i + delim + custom_key_mgr(j) ] = subvalues[j]
            elif isinstance(collection[i], list):
                subvalues = flatten_dict( collection[i], delim )
                for j in subvalues.keys():
                    val[ i + delim + custom_key_mgr(j) ] = subvalues[j]
                
                #for k in range(len(collection[i])):
                #    val[ i + delim + str(k) ] = flatten_dict(collection[i], delim)
            else:
                val[i] = collection[i]
    elif isinstance(collection, list):
        val = flatten_dict({str(i): flatten_dict(elmt, delim) for i, elmt in enumerate(collection)}, delim)
        pass
    else:
        ## Most of scalars and custom types are already handled above when the
        ## *original* call is given a collection. The recursion only takes
        ## the other routes.
        ##
        ## Now this is when the *original* call is like flatten...(42)
        ## or at when the end of a branch is reached.
        val = collection
        pass
    return val


################### Sorting ####################


def valuesForTrue(rule, values):
    """An helper generator to filter iterators. Unlike the filter function,
    it passes the index of the element in the iteration process.
    :param rule: Rule that says whether or 
            Either a list of booleans or a function taking (value, index) as arguments.
    :param values: iterator to filter
    :return: yields values that meet the rule
    """
    iterator = iter(values)
    val = next(iterator)
    try:
        _ = rule(val, 0)
        is_func = True
        filter_func = lambda x, i: rule(x, i)
    except:
        is_func = False
        # this way, external modification won't affect the generator
        rule = rule.copy()
        filter_func = lambda x, i: rule[i]  # bool(rule[i])
    
    # res = []
    shouldKeep = filter_func(val, 0)
    if shouldKeep:
        yield val
        # res.append(val)
    
    for i, val in enumerate(iterator):
        shouldKeep = filter_func(val, i + 1)  # the first value has was consummed
        if shouldKeep:
            # res.append(val)
            yield val
    # return res

def sortBasedOn(base, *toSort, reverse=False):
    """
    """
    base = list(base)
    perm = getPermutation(base, list(sorted(base)))
    
    res = []
    for arr in toSort:
        tmp = applyPermutation(arr, perm)
        if reverse:
            tmp = list(reversed(tmp))
        res.append(tmp)
    
    ## 
    if len(toSort) == 1:
        res = res[0]
    
    return res


def getPermutation(A, to):
    """
    uniqueIndexes: True/False: True
    """
    arr = A
    lastIndexSeen = dict( [(el,-1) for el in A] )
    p = []
    for i,el in enumerate(to):
        fromIndex = lastIndexSeen[el]+1
        theIndex = fromIndex + A[fromIndex:].index(el) # [0,1,2,3,0,1,2,3,4]
        lastIndexSeen[el] = theIndex
        p.append(theIndex)
    return p

def applyPermutation(arr, perm):
    dest = []
    for index in perm:
        dest.append( arr[index] )
    return dest

def sortedEffectif(eff, nis=None, reverse=False, returnSplitted=False):
    """
    :param nis:
    """
    # arr = [(k,eff[k]) for k in eff]
    # res = sorted(arr, key=lambda v: v[1], reverse=reverse)
    
    if isinstance(eff, dict):
        if isinstance(nis, bool) or isinstance(nis, int):
            returnSplitted, reverse = reverse, nis
        else:
            assert nis is None
        
        eff = list(eff.keys())
        nis = list(eff.values())
    elif isinstance(eff, list) and isinstance(nis, list):
        pass
    
    if nis:
        keys = eff
        counts = nis
    else:
        keys = [k for k in eff]
        counts = [eff[key] for key in keys]
    
    elmts = counts
    sortedElmts = sorted(counts, reverse=reverse)
    
    perm = getPermutation(elmts, sortedElmts)
    sortedKeys = applyPermutation(keys, perm)
    
    if returnSplitted:
        xis = sortedKeys
        nis = sortedElmts
        return xis, nis
        
    res = [(k, c) for k,c in zip(sortedKeys, sortedElmts)]
    return res

### Exemple d'utilisation des permutations
# brands = [art['brand'] for art in _targets]
# brandEffs = effectif(brands)
# brandEffs = [(key, brandEffs[key]) for key in brandEffs]
# _nbArts  = [pair[1] for pair in brandEffs]
# _marques = [pair[0] for pair in brandEffs]
# _sortedNbArts = sorted(_nbArts)
# _sortedNbArts.reverse()
# _perm = getPermutation(_nbArts, _sortedNbArts, uniqueIndexes=True)
# sortedBrands = applyPermutation(brandEffs, _perm)
# print(len(_targets))
# sortedBrands[:kNTopShortSellingBrands]
### >>>> outputs:
# [('HERMÈS', 1198),
#  ('CHANEL', 334),
#  ('LOUIS VUITTON', 209),
#  ('GUCCI', 174),
#  ('CÉLINE', 131),
#  ('SAINT LAURENT', 110),
#  ('CHLOÉ', 108),
#  ('ZADIG & VOLTAIRE', 68),
#  ...
#  ('ZARA', 41) ]



################### Secure filewrite (not interrupted with keyboard interrupt) ####################

def last_n_path_components(filepath, n, sep=None, trail=''):
    """
    """
    sep = os.path.sep if sep is None else sep
    parts = filepath.split(sep)[-n:]
    ## Idea for improving. If a trail is provided, then join
    ## a '/' with the trail. This reflexion comes from:
    # "..." -> ".../last/3/components"
    # but 
    # "" -> last/3/components
    # It would have wrong meaning if ".."
    #  
    trail = (trail + sep) if len(trail) > 0 else trail
    res = (trail + ) + os.path.join(*parts)
    return res
    


def _writeToFilepath(content, filepath, makeParents, binary=None, writeMode=None):
    """Helper function to write into a path
    :param content: the content you want to write to file
    :param writeMode: the write mode as you would provide to the open() function ("b" for binary, "a"
            for appending textual content, or "w" to replace textual content)
    """
    if not writeMode:
        if binary is None:
            binary = isinstance(content, bytes)
        writeMode = 'wb' if binary else 'w'
    
    content = content if binary or isinstance(content, str) else str(content)

    # avoid getting a FileNotFoundError if the path has the form "foo/bar"
    # but no error if no parent directory
    if makeParents and len(os.path.dirname(filepath)) > 0:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, writeMode) as of:
        of.write(content)


def writeFileWithoutInterruption(content, filepath, binaryWrite=None, writeMode=None, makeParents=True):
    """Writes a file without being affected by the user's Keyboard interruption (Ctrl+C / Cmd+C).
    This way, the file should be fully written before the program can finally exit as requested by the
    user.
    :param content: the content you want to write to file
    :param filepath: the filepath you want to save the file to.
    :param binaryWrite: whether the content is binary and you want to write binary content
    :param writeMode: the specific write mode you want, as you would provide to the open() function
            ("b" for binary, "a" for appending textual content, or "w" to replace textual content)
    """
    try:
        thr = Thread(target=_writeToFilepath, args=(content, filepath, makeParents, binaryWrite, writeMode))
        thr.start()
        thr.join()
    except KeyboardInterrupt as err:
        print("\n-- KeyboardInterrupt while a file is being written : interruption"
              " will occur after the writting process gets finished --\n "
              " (error: %s)" % str(err))


################### Others ####################


def description_of_dict_architecture(collection, keys_threshold, levels=None):
    """
    :param int keys_threshold: The maximum number of keys to allow when a dict
                level is too large. Dictionaries that have too many entries
                may be considered as an array so you can limit the amount
                of entries of each dict entry.
    :param int/None levels: the number of levels. Passing None will not limit
                the parsed tree.
    :rtype: dict / str
    :return: a dictionary 
    """
    # :param int/None indent: If you want the output as a string, you can pass in
    #             this parameter to transfer it to json.dumps.
    # assert isinstance(collection, dict) or isinstance(collection, list)
    
    next_level = None if (levels is None) else levels - 1
    
    ### I describe the first level and then call the function recursively
    
    def childs_have_similar_structure(collection):
        """Compares few child nodes to determine the pattern.
        For instance, what are the keys that are the most common...
        """
        assert False, "No IMP"
        return None
    
    def most_common_keys_of_children(collection):
        """
        """
        if isinstance(collection, list):
            result = {}
            
            content_types = [str(type(val)) for val in collection]
            stats = effectif(content_types, returnSplitted=False)
            
            distinct_content_types = set([str(type(val)).split("'")[1] for val in collection])
            
            if "list" not in distinct_content_types and "dict" not in distinct_content_types:
                # it only contains scalar types OR custom types
                result.update({"__stats__": "__keys-count__"})
                result.update({"__types__": "__array-of-scalar__"})
                result.update(stats)
                return result
            
            result.update({"__types__": "__array-of-any-type__"})
            result.update({"__stats__": "__keys-count__"})
            for i, value in enumerate(collection):
                ### Display the type
                # key = str(type(value)) if isinstance(value, dict) else value
                if isinstance(value, dict):
                    key = str(type(value))
                elif isinstance(value, list):
                    key = "%s :: %s" % (str(type(value)), (value[0] if len(value) > 0 else ""))
                else:
                    key = value
                
                ## 
                # if result.get(key) is not None:
                #     result[key] = result[key] + 1
                # else:
                #     result[key] = 1
                
                ### Display the keys of the subchild and show stats about
                ### the keys (how many times each subkey appears)
                if isinstance(value, dict):
                    for subkey in value:
                        if result.get(subkey) is not None:
                            result[subkey] = result[subkey] + 1
                            pass
                        else:
                            result[subkey] = 1
                            pass
                    pass
                pass
            
            return result
        else:
            assert False, "unhandled for now"
    
    
    result = {}
    
    if levels is None or levels > 0:
        if isinstance(collection, dict):
            
            ### In order to make the keys threshold matter,
            keys = list(collection)
            tmp = {}
            for key in keys:
                result[key] = description_of_dict_architecture(collection[key], keys_threshold, next_level)
            
            ### Dictionaries that have too many entries may be considered as
            ### an array so we limit their amount of entries
            if len(keys) > keys_threshold:
                surplus = len(keys) - keys_threshold
                keys_to_remove = sorted(keys[-surplus:])
                # while 
                # print("\n".join(sorted(keys_to_remove)))
                for key in keys_to_remove.copy():
                    # print("> removing '%s'" % (key))
                    del result[key]
                
                result["..."] = "..."  # add this key to signify the threshold has been reached
                pass
                        
        elif isinstance(collection, list):
            result = [most_common_keys_of_children(collection)]
            if len(collection) > 0:
                # tmp = collection[0]
                tmp = description_of_dict_architecture(collection[0], keys_threshold, next_level)
                result.append(tmp)
            pass
        
        else:
            # result = str(type(collection)).split("'")[1]
            result = "%s :: %s" % (str(type(collection)), collection)
    
    else:
        # result = str(type(collection)).split("'")[1]
        if isinstance(collection, dict) or isinstance(collection, list):
            result = "%s :: ..." % str(type(collection))  # trim the tree
        else:
            result = str(type(collection))
            ## may be too verbose if the value is like a numpy matrix
            # result = "%s :: %s" % (str(type(collection)), collection)
    
    return result


def splitToInts(arg, sep=','):
    """
    Convertis une chaîne de caractères contenant des entiers en une liste d'entiers.
    Retourne la liste d'entiers
    """
    components = arg.split(sep) if isinstance(arg,str) else arg;
    arr = [int(c) for c in components]
    return arr


def random_string(length, secure=False, characters=None):
    """Generates a random string
    :param length: length of the string to return
    :param bool secure: ... (see this answer: https://stackoverflow.com/a/23728630/4418092)
    :param characters: a collection of characters to construct the string with.
                Default will be all ASCII letters and numbers
    :return: a random string
    """
    # see this answer: https://stackoverflow.com/a/23728630/4418092
    characters = (string.ascii_uppercase + string.ascii_lowercase + string.digits) if characters is None else characters
    N = length
    if secure:
        s = ''.join( random.SystemRandom().choice(characters) for _ in range(N) )
    else:
        s = ''.join(random.choices(characters, k=N))
    return s

def make_random_string(length, secure=False, characters=None):
    return random_string(length, secure, characters)

# def recursivelyInspectKeys(aDict):
#     res = None
#     if isinstance(aDict, dict):
#         keys = list(dict)
#         for 
#     return keys


#### ---- Compatibility with camelCase code using this lib ---- ####

pad_symbols = padSymbols
pad_zeros_to_number = padZerosToNumber
strip_extra = stripExtra

pickleDumps = pickle_dumps
pickleLoads = pickle_loads
insert_in_file = insertInFile
base64Encode = base64_encode
base64Decode = base64_decode
urlEncode = url_encode
urlDecode = url_decode
replaceFileExtension = replace_file_extension

makeRandomString = make_random_string

weekdayNumber = weekday_number
hour_as_string = hourAsString
get_date_as_str = getDateAsStr
date_formatted_as_yma = dateFormattedAsYMA
date_to_datetime = dateToDatetime
datetime_to_date = datetimeToDate
split_to_ints = splitToInts
# date_from_components = dateFromComponents
hour_from_string = hourFromString

effectifU = effectif_u
concatenateSublists = concatenate_sublists
flattenList = flatten_list
flattenIterable = flatten_iterable
fillEmptyDictEntries = fill_empty_dict_entries
flattenDict = flatten_dict
flattenJson = flatten_json
splitEvenlyInIncreasingOrder = split_evenly_in_increasing_order

## Sorting
values_for_true = valuesForTrue
apply_permutation = applyPermutation
get_permutation = getPermutation
sort_based_on = sortBasedOn
sorted_effectif = sortedEffectif

write_file_without_interruption = writeFileWithoutInterruption
