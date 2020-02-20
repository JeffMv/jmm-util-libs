# -*- coding: utf-8 -*-
"""
"""

import os
import datetime

import pytest

# import jmm.divers as script
from .. import divers as script
# import divers as script


# def test_http_return(tmpdir, monkeypatch):
#     results = [{
#             "age": 84,
#             "agreeableness": 0.74
#           }
#         ]
    
#     def mockreturn(request):
#         return BytesIO(json.dumps(results).encode())

#     monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

#     p = tmpdir.mkdir("program").join("agents.json")
    
#     # run script
#     script.main(["--dest", str(p), "--count", "1"])

#     local_res = json.load(open(p))
#     assert local_res == script.get_agents(1)


################### Utils ####################

def test_pad_symbols():
    assert '0031' == script.padSymbols('31', 4, symbol=0, to_front=True)
    inputted = 'Hello everyone'
    width = len(inputted) + 5
    expected = 'Hello everyone!!!!!'
    assert expected == script.padSymbols(inputted, width, '!', False)

def test_pad_zeros_to_number():
    assert '03' == script.padZerosToNumber(3, 2)
    assert '12' == script.padZerosToNumber(12, 2)
    assert '000456' == script.padZerosToNumber(456, 6)

def test_strip_extra():
    ### Make sure to understand that it looks for *repetitions of a pattern*
    
    # Counter intuitive : recursive behaviour
    # recursively searching for remnants of the pattern
    inputted = "!!!!  ????  !!??!!??"
    count = 0
    expected = "!!!!  ????  "
    assert expected == script.stripExtra(inputted, '!?', count)
    
    # because it looks for '!?!?' because that's the *extra repetition*
    inputted = "!!!!????"
    arg = "!?"
    count = 1  # <-
    expected = "!!!!????"  # <-
    assert expected == script.stripExtra(inputted, arg, count)
    
    # it recursively searches the pattern and keeps 0 of the pattern at the end
    inputted = "!!!!????"
    arg = "!?"
    count = 0  # <-
    expected = ""  # <-
    assert expected == script.stripExtra(inputted, arg, count)
    
    inputted  = "  my  naaaaaame  is  Leeeeaaaaa"
    expected1  = "  my  name  is  Leeeea"
    expected2 = "  my  naaaaaame  is  Leeeeaaaaa"
    assert expected1 == script.stripExtra(inputted, 'a', 1)
    # because it looks for repetitions of "eaea"
    assert expected2 == script.stripExtra(inputted, 'ea', 1)
    
    # even or odd, it keeps the amount we want
    assert "Hi !!" == script.stripExtra("Hi !!!!!", '!', keep=2)
    assert "Hi !!" == script.stripExtra("Hi !!!!!!", '!', keep=2)
    assert "Hi !!!" == script.stripExtra("Hi !!!!!!", '!', keep=3)
    assert "Hi !!!" == script.stripExtra("Hi !!!!!!!", '!', keep=3)
    assert "Hi !!!" == script.stripExtra("Hi !!!!!!!!", '!', keep=3)
    
    inputted = "... story of bananas bananas and fruits"
    arg1 = ' bananas'
    arg2 = ' bananas '
    expected1 = "... story of bananas and fruits"
    expected2 = "... story of bananas bananas and fruits"
    assert expected1 == script.stripExtra(inputted, arg1, 1)
    assert expected2 == script.stripExtra(inputted, arg2, 1)
    
    count = 0
    assert 'Hello!' == script.stripExtra("Hello World !", " World ", count)


################### Files, folders and encoding ####################

def test_replace_file_extension():
    inputted = "/path/to/file.PNG"
    expected = "/path/to/file.jpg"
    assert expected == script.replace_file_extension(inputted, 'jpg')
    
    inputted = "/path/to.png/file.png"
    expected = "/path/to.png/file.JPG"
    assert expected == script.replace_file_extension(inputted, 'JPG')

def test_append_to_basename():
    inputted = "/path/to/basename.exe"
    expected = "/path/to/basename-file.exe"
    assert expected == script.append_to_basename(inputted, '-file')
    
    inputted = ".secret/directory"
    expected = ".secret/directory-stealth"
    assert expected == script.append_to_basename(inputted, '-stealth')
    
    # "alone" is not an extension here
    inputted = ".alone"
    expected = ".alone-expected"
    assert expected == script.append_to_basename(inputted, '-expected')
    
    with pytest.raises(ValueError):  # feel free to change the exception type
        script.append_to_basename("path/..value", 'anything')


@pytest.mark.skip(reason="YAGNI. And might be bothersome to test. What would be a *good* test and test design for this?")
def test_insertInFile():
    ### TEST IS NOT DONE
    # how to proceed with testing. And what about with line returns (Unix/Dos)
    # example_content = """URL Encoding (Percent Encoding)\nHello world"""
    script.insertInFile
    assert False


################### Dates and times ####################

def test_hour_as_string():
    assert "19h11" == script.hour_as_string(datetime.datetime(2016, 10, 1, 19, 11))
    assert "02h01" == script.hour_as_string(datetime.datetime(2019, 10, 1, 2, 1, 34))

def test_hour_from_string():
    assert (3, 45) == script.hour_from_string("03h45")
    # assert (3, 45) == script.hour_from_string("3h45")
    # assert (3, 45) == script.hour_from_string("\n\n 3h45    \n   ")
    assert (19, 5) == script.hour_from_string("19:05")
    assert (7, 13) == script.hour_from_string("07:13")
    
    # assert (7, 13, 0) == script.hour_from_string("07:13:00")
    # assert (7, 13, 0) == script.hour_from_string("07h13m00s")
    assert None == script.hour_from_string("07:13:00")
    assert None == script.hour_from_string("07h13m00s")
    
    assert None == script.hour_from_string("3h45")
    assert None == script.hour_from_string("\n\n 3h45    \n   ")
    
    # assert None == script.hour_from_string("3h45 4h10")
    # with pytest.raises(ValueError):
    #   _ = script.hour_from_string("3h45 4h10")
    # with pytest.raises(ValueError):
    #   _ = script.hour_from_string(None)
    # with pytest.raises(ValueError):
    #   _ = script.hour_from_string(1230)


def test_get_date_as_str():
    assert "2016-01-01" == script.get_date_as_str(datetime.datetime(2016, 1, 1, 19, 11))
    assert "2018-11-09" == script.get_date_as_str(datetime.date(2018, 11, 9))
    assert "1993-07-30" == script.get_date_as_str(datetime.date(1993, 7, 30))

def test_date_formatted_as_yma():
    assert "2016-01-01" == script.date_formatted_as_yma(datetime.datetime(2016, 1, 1, 19, 11))
    assert "2019-11-09" == script.date_formatted_as_yma(datetime.date(2019, 11, 9))
    assert "2017.07.30" == script.date_formatted_as_yma(datetime.date(2017, 7, 30), '.')

def test_weekday_number():
    # a sunday, then monday, tuesday, wed, thursday, friday, saturday, sunday
    assert 6 == script.weekday_number(datetime.date(2019, 8, 4))
    assert 0 == script.weekday_number(datetime.date(2019, 8, 5))
    assert 1 == script.weekday_number(datetime.date(2019, 8, 6))
    assert 2 == script.weekday_number(datetime.date(2019, 8, 7))
    assert 3 == script.weekday_number(datetime.date(2019, 1, 3))
    assert 4 == script.weekday_number(datetime.date(2019, 1, 25))
    assert 5 == script.weekday_number(datetime.date(2018, 10, 27))
    assert 6 == script.weekday_number(datetime.date(2018, 10, 28))
    # thursday, tue, sat
    assert 2 == script.weekday_number(datetime.date(2018, 2, 28))
    assert 0 == script.weekday_number(datetime.date(2016, 2, 29))
    assert 5 == script.weekday_number(datetime.date(2020, 2, 29))

def test_date_to_datetime():
    assert datetime.datetime(2020, 2, 29) == script.date_to_datetime(datetime.date(2020, 2, 29))
    assert datetime.datetime(1392, 1, 29) == script.date_to_datetime(datetime.datetime(1392, 1, 29))
    assert datetime.date(2020, 2, 29) != script.date_to_datetime(datetime.datetime(2020, 2, 29))
    assert datetime.date(2020, 2, 29) != script.date_to_datetime(datetime.date(2020, 2, 29))


def test_datetime_to_date():
    assert datetime.date(2020, 2, 29) == script.datetime_to_date(datetime.datetime(2020, 2, 29))
    assert datetime.date(2020, 2, 29) == script.datetime_to_date(datetime.date(2020, 2, 29))
    assert datetime.datetime(2020, 2, 29) != script.datetime_to_date(datetime.date(2020, 2, 29))
    assert datetime.datetime(2020, 2, 29) != script.datetime_to_date(datetime.datetime(2020, 2, 29))


# def test_date_from_components():
#   assert datetime. == script.date_from_components((2020, 2, 29), None, '-')
#   assert False



###

def _helper_compare_dicts(d1, d2, func, default):
    """
    helper to compare values of a dictionary by simple call.
    :param default: the value to use if a dict does not have a key the other has.
    """
    results = []
    for key in (set(d1.keys()) | set(d2.keys())):
        v1, v2 = d1.get(key, default), d2.get(key, default)
        results.append(func(v1, v2))
    return results


def test_frequency():
    sample = [0, 0, 1,1,1,1,1 , 15, 30, 30, 30, -4, 15,15,15]
    expected_keys = [-4, 0, 1, 15, 30]
    expected_values = [1, 2, 5, 4, 3]
    expected_probabilities = [1/15, 2/15, 5/15, 4/15, 3/15]
    
    ## NOTE: be cautious when adding complex code in unit tests, but i'm sure
    ##      that this does what we want without error
    ##      i.e. takes 2 collections and turn them into a dict with keys
    ##      and the second values
    # to_dict = lambda keys, values: (len(keys) == len(values)) and {key: val for key, val in zip(keys, values)}
    def to_dict(keys, values):
        assert (len(keys) == len(values)), "non-matching lengths"
        return {key: val for key, val in zip(keys, values)}
    
    expected_unsorted = to_dict(expected_keys, expected_values)
    expected_unsorted_probabilities = to_dict(expected_keys, expected_probabilities)
    
    ### testing UNsorted result:
    ## since (theoritically) the order of the output collections should NOT
    ## be expected to be consistent (since that specification is not part of
    ## the API) we make additional checks to ensure we do NOT just assume
    ## a consistent order.
    
    # using an unordered collection to make the code easier to read and
    # solve the problem specified above
    xis, nis = script.frequency(sample)
    assert to_dict(xis, nis) == expected_unsorted
    xis, nis = script.frequency(sample, probabilities=False)
    assert to_dict(xis, nis) == expected_unsorted
    
    
    ## testing probabilities (float comparison implied)
    xis, pis = script.frequency(sample, probabilities=True)
    # NOTE: the following two asserts compare separately keys and values
    #       and thus lack to ensure that each
    assert set(xis) == set(expected_keys)
    results = _helper_compare_dicts(to_dict(xis, nis), expected_unsorted, (lambda x,y: pytest.approx(x) == y), None)
    # print(f"pis, expected_probabilities: \n{pis} \n{expected_probabilities}")
    # results = [pytest.approx(pair[0], 1/15) == pair[1] for pair in zip(pis, expected_probabilities)]
    assert all(results)
    # assert all(list(map(lambda tup: pytest.approx(tup[0]) == tup[1], zip(pis, expected_probabilities))))
    
    computed = to_dict(xis, pis)
    assert set(computed.keys()) == set(expected_unsorted.keys())
    for key in computed:
        value = computed.get(key)
        assert pytest.approx(value) == expected_unsorted_probabilities[key], f"comparison failed for key {key}"
        pass
    
    
    ### testing with OPTION : SORT=True
    # caution: the "sort" option sorts based on the number of elements in the collection.
    # AND sort order beyond the number of elements is not specified.
    # (for instance if
    # both 1 and 15 are each found 3 times in the sample, the order in which 1 and 15
    # will apear in sorted_xis is not specified).
    # That order is now only deterministic/predictable due to implementation details.
    expected_keys_ordered_by_value_count = [-4, 0, 30, 15, 1]
    expected_values_ordered_by_value_count = [1, 2, 3, 4, 5]  # <- keys are sorted by these values
    sorted_xis, sorted_nis = script.frequency(sample, probabilities=False, sort=True)
    assert sorted_xis == expected_keys_ordered_by_value_count
    assert sorted_nis == expected_values_ordered_by_value_count
    
    expected_probabilities_ordered_by_value_count = [1/15, 2/15, 3/15, 4/15, 5/15]  # <- keys are sorted by these values
    sorted_xis, sorted_pis = script.frequency(sample, probabilities=True, sort=True)
    assert sorted_xis == expected_keys_ordered_by_value_count  
    assert len(sorted_xis) == len(sorted_pis)
    for i, key in enumerate(sorted_xis):
        expected = expected_probabilities_ordered_by_value_count[i]
        assert (pytest.approx(sorted_pis[i]) == expected), f"key {key} do not have expected value"


# def test_effectif():
#     sample = [0, 0, 1,1,1,1,1 , 15, 30, 30, 30, -4, 15,15,15]
#     expected_keys = [-4, 0, 1, 15, 30]
#     expected_values = [1, 2, 5, 4, 3]
    
#     xis, nis = script.effectif(sample, returnSplitted=True)
#     ## We do not expect the output of the function to be sorted since it might be time consuming
#     sorted_xis = sorted(xis)
#     assert expected_keys == sorted_xis
#     for i, x in enumerate(sorted_xis):
#         assert expected_values[i] == nis[xis.index(x)]
#     # assert ([-4,0,1,15,30], [2,5,1,3]) = (list(sorted(xis)))
#     # assert ([-4,0,1,15,30], [1,1,1,1]) = script.effectif(set(sample), returnSplitted=True)
    
#     script.effectif
#     script.effectif(sample, True)
#     assert False


@pytest.mark.skip(reason="no way of currently testing this")
def test_frequences():
    script.frequences
    assert False

@pytest.mark.skip(reason="not testing this because of YAGNI")
def test_effectif_u():
    script.effectif_u
    assert False

@pytest.mark.skip(reason="not testing this because of YAGNI. See tests for frequency()")
def test_sortedEffectif():
    script.sortedEffectif
    assert False


###


def test_flattening_iterables():
    array = [[1, 2], [-1, 'a'], ['cowoiew', "ineogfe", "iofnefoe"]]
    expected = [1, 2, -1, 'a', 'cowoiew', "ineogfe", "iofnefoe"]
    assert script.concatenate_sublists(array) == expected
    assert script.flatten_iterable(array) == expected
    assert script.flatten_iterable(iter(array)) == expected
    
    array = [[1, 2, [300, 500, [123456]]], [-1, ['bonjour', 'hello'], 'a'], ['cowoiew', "ineogfe", "iofnefoe"]]
    expected = [1, 2, [300, 500, [123456]], -1, ['bonjour', 'hello'], 'a', 'cowoiew', "ineogfe", "iofnefoe"]
    assert script.concatenate_sublists(array) == expected
    assert script.flatten_iterable(array) == expected
    assert script.flatten_iterable(iter(array)) == expected
    
    array = [[0, [], ['ofefow']], 12, [-1, 'a'], [1000, 4444]]
    expected = [0, [], ['ofefow'], 12, -1, 'a', 1000, 4444]
    with pytest.raises(TypeError):
        # only handles arrayays, not single values like 12 or other types of iterables
        assert script.concatenate_sublists(array)
    
    assert script.flatten_iterable(array) == expected
    assert script.flatten_iterable(iter(array)) == expected
    
    # Maybe more tests should be added, both for usage expectation and
    # spotting potential errors.
    # Such tests may include, but not limited to:
    # - input testing: errors raised ?
    # - more complex flattening
    # assert False


def test_split_evenly_in_increasing_order():
    array = list(range(20, 31))
    groups = 1
    expected = [array]
    assert expected == script.split_evenly_in_increasing_order(array, groups)
    
    array = list(range(20, 31))
    groups = 3
    expected = [[20,23,26,29],[21,24,27,30],[22,25,28]]
    assert expected == script.split_evenly_in_increasing_order(array, groups)
    
    groups = 2
    expected = [list(range(20, 31, 2)), list(range(21, 31, 2))]
    assert expected == script.split_evenly_in_increasing_order(array, groups)
    
    array = list(range(20, 30))
    groups = 2
    expected = [list(range(20, 30, 2)), list(range(21, 30, 2))]
    assert expected == script.split_evenly_in_increasing_order(array, groups)
    
    groups = 3
    expected = [[20,23,26,29],[21,24,27],[22,25,28]]
    assert expected == script.split_evenly_in_increasing_order(array, groups)


@pytest.mark.skip(reason="not testing this because of YAGNI")
def test_fill_empty_dict_entries():
    script.fill_empty_dict_entries
    assert False


def test_flatten_dict():
    expected = {
        'a__subA': 'hello', 
        'a__myarray__0': 'Hi',
        'a__myarray__1': 'dear',
        'b': 12,
        '49__hello': 'world'}
    
    inputted = {
        "a": {
            "subA": "hello",
            "myarray": [
                "Hi",
                "dear"
            ]
        },
        "b": 12,
        "49": {"hello": "world"}}
    result = script.flatten_json(inputted, "__")
    assert expected == result
    
    ## Check that it behaves well for arrays
    # expected = {"a":{}, "b": {}}
    # expected = ["a", ""]
    # inputted = {
    #   "0": "a",
    #   "1----b": ""
    # }

    inputted = ["a", {"b": ""}]
    expected = {
        "0": "a",
        "1----b": ""
    }
    result = script.flatten_json(inputted, "----")
    assert expected == result
    
    pass


def test_valuesForTrue():
    array = list(range(-1, 10))
    arg = lambda x, i: i % 2 == 0  # even INDEXES
    expected = [-1, 1, 3, 5, 7, 9]
    assert expected == list(script.valuesForTrue(arg, array))
    
    array = list(range(995, 1001))
    arg = lambda x, i: i % 2 == 0  # even INDEXES
    expected = [995, 997, 999]
    assert expected == list(script.valuesForTrue(arg, array))
    
    arg = lambda x, i: x % 2 == 0  # even NUMBERS
    expected = [996, 998, 1000]
    assert expected == list(script.valuesForTrue(arg, array))
    
    arg = [True, False, False, 0, 0, 1]
    expected = [995, 1000]
    assert expected == list(script.valuesForTrue(arg, array))


def test_sortBasedOn():
    array = ["Salamander", ".1nd", 314, -134, [], 3993]
    inputted = [4, 5, 0, 10000, -999, -10]
    ordered_input = list(sorted(inputted))
    expected = [[], 3993, 314, "Salamander", ".1nd", -134]
    assert [ordered_input, expected] == script.sortBasedOn(inputted, array)
    
    array = ["Salamander", ".1nd", 314, -134, [], 3993]
    inputted = [4, 5, 0, 10000, -999, -10]
    second_input = ["delta", "espilon", "gamma", "zeta", "alpha", "beta"]
    ordered_input = list(sorted(inputted))
    expected = [[], 3993, 314, "Salamander", ".1nd", -134]
    second_expected_output = ['alpha', 'beta', 'gamma', 'delta', 'espilon', 'zeta']
    assert [ordered_input, expected, second_expected_output] == script.sortBasedOn(inputted, array, second_input)
    
    

def test_getPermutation():
    inputted = [4, 5, 0, 10000, -999, -10]
    array = list(sorted(inputted))
    # the permutation we need to apply to get array
    expected = [4, 5, 2, 0, 1, 3]
    assert expected == script.getPermutation(inputted, array)

def test_applyPermutation():
    inputted = [4, 5, 0, 10000, -999, -10]
    # a permutation that will sort the inputted in increasing order
    permutation = [4, 5, 2, 0, 1, 3]
    expected = list(sorted(inputted))
    assert expected == script.applyPermutation(inputted, permutation)


# def test_writeFileWithoutInterruption():
#   script.writeFileWithoutInterruption
#   assert False

# def test_noInterruptFileWrite():
#   script.noInterruptFileWrite
#   assert False

def test_description_of_dict_architecture():
    inputted = {1:100, 2:[], 3:{}}
    levels = None
    threshold = 0
    assert len(script.description_of_dict_architecture(inputted, threshold, levels)) == 1
    threshold = 1
    assert len(script.description_of_dict_architecture(inputted, threshold, levels)) == 2
    
    inputted = {1:100, 2:[], 3:{}}
    threshold = 50
    arg1 = 0
    arg2 = 1
    expected1 = "<class 'dict'> :: ..."
    expected2 = {1: "<class 'int'>", 2: "<class 'list'> :: ...", 3: "<class 'dict'> :: ..."}
    assert expected1 == script.description_of_dict_architecture(inputted, threshold, arg1)
    assert expected2 == script.description_of_dict_architecture(inputted, threshold, arg2)
    
    inputted = {1:100, 2:[], 3:["a", "b", "c", "a", "c", "c"], 4:{}}
    levels = None
    # expected = { 1: "<class 'int'> :: 100",
    #   2: [{'__stats__': '__keys-count__', '__types__': '__array-of-scalar__'}],
    #   3: [{'__stats__': '__keys-count__', '__types__': '__array-of-scalar__'},
    #       {'a': 2, 'b': 1, 'c': 3}],
    #   4: {}
    #   }
    expected = {1: "<class 'int'> :: 100",
        2: [{'__stats__': '__keys-count__', '__types__': '__array-of-scalar__'}],
        3: [{"<class 'str'>": 6,
             '__stats__': '__keys-count__',
             '__types__': '__array-of-scalar__'},
            "<class 'str'> :: a"],
        4: {}}
    # expected = {}
    assert expected == script.description_of_dict_architecture(inputted, threshold, levels)
    
    # Maybe more tests should be added, both for usage expectation and
    # spotting potential errors.
    # Such tests may include, but not limited to:
    # - input testing: errors raised ?
    # - more complex descriptions
    # assert False


def test_split_to_ints():
    inputted = "12-23-34-49-50"
    expected = [12, 23, 34, 49, 50]
    assert expected == script.split_to_ints(inputted, "-")
    
    inputted = "13, 0, -314, 10000,1000,-50"
    expected = [13, 0, -314, 10000, 1000, -50]
    assert expected == script.split_to_ints(inputted, ",")
    
    with pytest.raises(ValueError):
        script.split_to_ints("12.3-10000-300")

def test_make_random_string():
    ## Ensure random strings should not be repeated
    # ensure the
    lengths = [5, 10]
    results = []
    for length in lengths:
        for i in range(20):
            tmp = script.make_random_string(length)
            assert len(tmp) == length
            assert tmp not in results
            results.append(tmp)
    
