# -*- coding: utf-8 -*-

"""
Tests for camel_tools.utils.stringutils
"""

from __future__ import absolute_import, print_function

import six

from camel_tools.utils import isUnicode


class TestIsUnicodeString(object):
    """Test class for testing the isUnicode function.
    """

    def test_isunicodestring_none(self):
        """Test that None is not a unicdoe string.
        """

        assert not isUnicode(None)

    def test_isunicodestring_int(self):
        """Test that int (a primitive type) is not a unicode string.
        """

        assert not isUnicode(0)

    def test_isunicodestring_list(self):
        """Test that a list (a Python object) is not a unicode string.
        """

        assert not isUnicode(['hello', 'world'])

    def test_isunicodestring_byte(self):
        """Test that an explicit byte string is not a Unicode string.
        """

        assert not isUnicode(b'Hello, world!')

    def test_isunicodestring_str(self):
        """Test that the default string type in Python 3 is a unicode string
        but not in Python 2.
        """

        # In Python 3 strings are unicode encoded by default.
        if six.PY3:
            assert isUnicode('Hello, world!')
        else:
            assert not isUnicode('Hello, world!')

    def test_isunicodestring_unicode(self):
        """Test that a unicode literal is a unicode string.
        """

        assert isUnicode(u'Hello, world!')
