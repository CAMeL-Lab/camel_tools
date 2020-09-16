# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2020 New York University Abu Dhabi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Tests for camel_tools.utils.charmap
"""

from __future__ import absolute_import, print_function

from collections.abc import Mapping

import pytest

from camel_tools.utils.charmap import CharMapper
from camel_tools.utils.charmap import InvalidCharMapKeyError
from camel_tools.utils.charmap import BuiltinCharMapNotFoundError


# A valid map used for testing CharMapper.map_string
VALID_MAP = {
    'e': 'u',
    'h-m': '*',
    'a-d': 'm',
    '٠': '0',
    '١': '1',
    '\u0662': '2',
    '\u0663-\u0665': '-',
    '٦-٩': '+'
}


class AnotherMapping(Mapping):
    """A class that subclasses collections.Mappings.
    """
    def __init__(self):
        self._dict = {}

    def __getitem__(self, key):
        return self._dict.__getitem__(key)

    def __setitem__(self, key, value):
        return self._dict.__setitem__(key, value)

    def __iter__(self):
        return self._dict.__iter__()

    def __len__(self):
        return self._dict.__len__()


class TestCharMapperInit(object):
    """Test class for testing CharMapper initialization.
    """

    def test_init_none(self):
        """Test that init with None raises a TypeError.
        """

        with pytest.raises(TypeError):
            CharMapper(None)

    def test_init_empty_dict(self):
        """Test that init with an empty dict doesn't raise an exception.
        """

        assert CharMapper({})

    def test_init_dictlike_object(self):
        """Test that init with an dict-like object doesn't raise an exception.
        """

        assert CharMapper(AnotherMapping())

    def test_init_not_dict(self):
        """Test that a non-dict object (list) raises a TypeError.
        """

        with pytest.raises(TypeError):
            CharMapper([])

    def test_init_default_not_valid1(self):
        """Test that an invalid type (list) for default raises a TypeError.
        """

        with pytest.raises(TypeError):
            CharMapper({}, [])

    def test_init_default_not_valid2(self):
        """Test that an invalid type (byte string) for default raises a
        TypeError.
        """

        with pytest.raises(TypeError):
            CharMapper({}, b'Hello')

    def test_init_default_valid1(self):
        """Test that a None type for default doesn't raise an Exception.
        """

        assert CharMapper({}, None)

    def test_init_default_valid2(self):
        """Test that a Unicode string type for default doesn't raise an
        Exception.
        """

        assert CharMapper({}, 'Hello')

    def test_init_charmap_valid1(self):
        """Test that a valid charMap doesn't raise an Exception.
        """

        assert CharMapper({'a': 'Hello'})

    def test_init_charmap_valid2(self):
        """Test that a valid charMap doesn't raise an Exception.
        """

        assert CharMapper({'a': None})

    def test_init_charmap_valid3(self):
        """Test that a valid charMap doesn't raise an Exception.
        """

        assert CharMapper({'a-f': ''})

    def test_init_charmap_valid4(self):
        """Test that a valid charMap doesn't raise an Exception.
        """

        assert CharMapper({'a-f': '', 'b': None}, 'Hello')

    def test_init_charmap_valid5(self):
        """Test that a valid charMap doesn't raise an Exception.
        """
        assert CharMapper({'--a': ''})

    def test_init_charmap_invalid1(self):
        """Test that an invalid key (byte string) type in charMap raises a
        TypeError.
        """

        with pytest.raises(TypeError):
            CharMapper({b'a': 'Hello'})

    def test_init_charmap_invalid2(self):
        """Test that an invalid value type (byte string) for a valid key
        (single Unicode character) in charMap raises a TypeError.
        """

        with pytest.raises(TypeError):
            CharMapper({'a': b'Hello'})

    def test_init_charmap_invalid3(self):
        """Test that an invalid value type (byte string) for an invalid key
        (Unicode character range with wrong order) in charMap raises a
        InvalidCharMapKeyError.
        """

        with pytest.raises(InvalidCharMapKeyError):
            CharMapper({'c-a': b'Hello'})

    def test_init_charmap_invalid4(self):
        """Test that an invalid value type (byte string) for an invalid key
        (neither a single Unicode character nor a Unicode character range) in
        charMap raises a InvalidCharMapKeyError.
        """

        with pytest.raises(InvalidCharMapKeyError):
            CharMapper({'cdsn': b'Hello'})

    def test_init_charmap_invalid5(self):
        """Test that an invalid key (neither a single Unicode character nor a
        Unicode character range) in charMap raises a InvalidCharMapKeyError.
        """

        with pytest.raises(InvalidCharMapKeyError):
            CharMapper({'a-': 'Hello'})

    def test_init_charmap_invalid6(self):
        """Test that an invalid key (neither a single Unicode character nor a
        Unicode character range) in charMap raises a InvalidCharMapKeyError.
        """

        with pytest.raises(InvalidCharMapKeyError):
            CharMapper({'a--': 'Hello'})

    def test_init_charpap_invalid7(self):
        """Test that an invalid key (neither a single Unicode character nor a
        Unicode character range) in charMap raises a InvalidCharMapKeyError.
        """

        with pytest.raises(TypeError):
            CharMapper({'--a': b'Hello'})


class TestCharMapperMapString(object):
    """Test class for testing CharMapper's map_string method.
    """

    def test_mapstring_none(self):
        """Test that a None value causes the map_string method to raise a
        TypeError.
        """

        with pytest.raises(TypeError):
            mapper = CharMapper(VALID_MAP)
            mapper.map_string(None)

    def test_mapstring_empty_string(self):
        """Test that an empty string causes the map_string method to return an
        empty string.
        """

        mapper = CharMapper(VALID_MAP)
        assert mapper.map_string('') == ''

    def test_mapstring_not_unicode(self):
        """Test that a non-unicode string causes the map_string method to raise
        a TypeError.
        """

        with pytest.raises(TypeError):
            mapper = CharMapper(VALID_MAP)
            mapper.map_string(b'Hello, world!')

    def test_mapstring_english(self):
        """Test that a map_string properly maps an English unicode string.
        """

        mapper = CharMapper(VALID_MAP)
        assert mapper.map_string('Hello, world!') == 'Hu**o, wor*m!'

    def test_mapstring_arabic(self):
        """Test that a map_string properly maps an Arabic unicode string.
        """
        mapper = CharMapper(VALID_MAP)
        assert mapper.map_string('٠١٢٣٤٥٦٧٨٩') == '012---++++'


class TestCharMapperBuiltinMapper(object):
    """Test class for testing CharMapper's builtin_mapper method.
    """

    def test_builtinmapper_ar2bw(self):
        """Test that the builtin 'ar2bw' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('ar2bw')

    def test_builtinmapper_ar2safebw(self):
        """Test that the builtin 'ar2safebw' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('ar2safebw')

    def test_builtinmapper_ar2xmlbw(self):
        """Test that the builtin 'ar2xmlbw' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('ar2xmlbw')

    def test_builtinmapper_ar2hsb(self):
        """Test that the builtin 'ar2hsb' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('ar2bw')

    def test_builtinmapper_bw2ar(self):
        """Test that the builtin 'bw2ar' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('bw2ar')

    def test_builtinmapper_bw2safebw(self):
        """Test that the builtin 'bw2safebw' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('bw2safebw')

    def test_builtinmapper_bw2xmlbw(self):
        """Test that the builtin 'bw2xmlbw' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('bw2xmlbw')

    def test_builtinmapper_bw2hsb(self):
        """Test that the builtin 'bw2hsb' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('bw2hsb')

    def test_builtinmapper_safebw2ar(self):
        """Test that the builtin 'safebw2ar' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('safebw2ar')

    def test_builtinmapper_safebw2bw(self):
        """Test that the builtin 'safebw2bw' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('safebw2bw')

    def test_builtinmapper_safebw2xmlbw(self):
        """Test that the builtin 'safebw2xmlbw' scheme is loaded without
        errors.
        """

        assert CharMapper.builtin_mapper('safebw2xmlbw')

    def test_builtinmapper_safebw2hsb(self):
        """Test that the builtin 'safebw2hsb' scheme is loaded without
        errors.
        """

        assert CharMapper.builtin_mapper('safebw2hsb')

    def test_builtinmapper_xmlbw2ar(self):
        """Test that the builtin 'xmlbw2ar' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('xmlbw2ar')

    def test_builtinmapper_xmlbw2bw(self):
        """Test that the builtin 'xmlbw2bw' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('xmlbw2bw')

    def test_builtinmapper_xmlbw2safebw(self):
        """Test that the builtin 'xmlbw2safebw' scheme is loaded without
        errors.
        """

        assert CharMapper.builtin_mapper('xmlbw2safebw')

    def test_builtinmapper_xmlbw2hsb(self):
        """Test that the builtin 'xmlbw2hsb' scheme is loaded without
        errors.
        """

        assert CharMapper.builtin_mapper('xmlbw2hsb')

    def test_builtinmapper_hsb2ar(self):
        """Test that the builtin 'hsb2ar' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('hsb2ar')

    def test_builtinmapper_hsb2bw(self):
        """Test that the builtin 'hsb2bw' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('hsb2bw')

    def test_builtinmapper_hsb2safebw(self):
        """Test that the builtin 'hsb2safebw' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('hsb2safebw')

    def test_builtinmapper_hsb2xmlbw(self):
        """Test that the builtin 'hsb2xmlbw' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('hsb2xmlbw')

    def test_builtinmapper_arclean(self):
        """Test that the builtin 'arclean' scheme is loaded without errors.
        """

        assert CharMapper.builtin_mapper('arclean')

    def test_builtinmapper_invalid(self):
        """Test that an invalid builtin scheme name raises a
        BuiltinCharMapNotFound exception.
        """

        with pytest.raises(BuiltinCharMapNotFoundError):
            CharMapper.builtin_mapper('hello')
