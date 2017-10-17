# -*- coding: utf-8 -*-

"""
Tests for camel_tools.utils.charmap
"""

from __future__ import absolute_import, print_function

from collections import Mapping

import pytest

from camel_tools.utils import CharMapper, InvalidCharMapKeyError


validMap = {
    u'e': u'u',
    u'h-m': u'*',
    u'a-d': u'm',
    u'٠': u'0',
    u'١': u'1',
    u'\u0662': u'2',
    u'\u0663-\u0665': u'-',
    u'٦-٩': u'+'
}


class AnotherMapping(Mapping):

    def __init__(self):
        self.d = {}

    def __getitem__(self, key):
        return self.d.__getitem__(key)

    def __setitem__(self, key, value):
        return self.d.__setitem__(key, value)

    def __iter__(self):
        return self.d.__iter__()

    def __len__(self):
        return self.d.__len__()


class TestCharMapper(object):

    def test_init_None(self):
        with pytest.raises(TypeError):
            CharMapper(None)

    def test_init_emptyDict(self):
        assert(CharMapper({}))

    def test_init_dictLikeObject(self):
        assert(CharMapper(AnotherMapping()))

    def test_init_notADict(self):
        with pytest.raises(TypeError):
            CharMapper([])

    def test_init_defaultNotValid1(self):
        with pytest.raises(TypeError):
            CharMapper({}, [])

    def test_init_defaultNotValid2(self):
        with pytest.raises(TypeError):
            CharMapper({}, b'Hello')

    def test_init_defaultValid1(self):
        assert(CharMapper({}, None))

    def test_init_defaultValid2(self):
        assert(CharMapper({}, u'Hello'))

    def test_init_charMapValid1(self):
        assert(CharMapper({u'a': u'Hello'}))

    def test_init_charMapValid2(self):
        assert(CharMapper({u'a': None}))

    def test_init_charMapValid3(self):
        assert(CharMapper({u'a-f': u''}))

    def test_init_charMapValid4(self):
        assert(CharMapper({u'a-f': u'', u'b': None}, u'Hello'))

    def test_init_charMapValid5(self):
        assert(CharMapper({u'--a': u''}))

    def test_init_charMapInvalid1(self):
        with pytest.raises(TypeError):
            CharMapper({b'a': u'Hello'})

    def test_init_charMapInvalid2(self):
        with pytest.raises(TypeError):
            CharMapper({u'a': b'Hello'})

    def test_init_charMapInvalid3(self):
        with pytest.raises(InvalidCharMapKeyError):
            CharMapper({u'c-a': b'Hello'})

    def test_init_charMapInvalid4(self):
        with pytest.raises(InvalidCharMapKeyError):
            CharMapper({u'cdsn': b'Hello'})

    def test_init_charMapInvalid5(self):
        with pytest.raises(InvalidCharMapKeyError):
            CharMapper({u'a-': u'Hello'})

    def test_init_charMapInvalid6(self):
        with pytest.raises(InvalidCharMapKeyError):
            CharMapper({u'a--': u'Hello'})

    def test_init_charMapInvalid7(self):
        with pytest.raises(TypeError):
            CharMapper({u'--a': b'Hello'})

    def test_mapString_None(self):
        with pytest.raises(TypeError):
            mapper = CharMapper(validMap)
            mapper.mapString(None)

    def test_mapString_emptyString(self):
        mapper = CharMapper(validMap)
        assert(mapper.mapString(u'') == u'')

    def test_mapString_notUnicode(self):
        with pytest.raises(TypeError):
            mapper = CharMapper(validMap)
            mapper.mapString(b'Hello, world!')

    def test_mapString_english(self):
        mapper = CharMapper(validMap)
        assert(mapper.mapString(u'Hello, world!') == u'Hu**o, wor*m!')

    def test_mapString_arabic(self):
        mapper = CharMapper(validMap)
        assert(mapper.mapString(u'٠١٢٣٤٥٦٧٨٩') == u'012---++++')
