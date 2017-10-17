# -*- coding: utf-8 -*-

"""
Tests for camel_tools.utils.stringutils
"""

from __future__ import absolute_import, print_function

import six

from camel_tools.utils import isUnicode


class TestIsUnicodeString(object):

    def test_isUnicodeString_None(self):
        assert not isUnicode(None)

    def test_isUnicodeString_int(self):
        assert not isUnicode(0)

    def test_isUnicodeString_list(self):
        assert not isUnicode(['hello', 'world'])

    def test_isUnicodeString_byte(self):
        assert not isUnicode(b'Hello, world!')

    def test_isUnicodeString_str(self):
        # In Python 3 strings are unicode encoded by default.
        if six.PY3:
            assert isUnicode('Hello, world!')
        else:
            assert not isUnicode('Hello, world!')

    def test_isUnicodeString_unicode(self):
        assert isUnicode(u'Hello, world!')
