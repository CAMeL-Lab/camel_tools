# -*- coding: utf-8 -*-

"""
Tests for camel_tools.utils.stringutils
"""

from __future__ import absolute_import, print_function

import six

from camel_tools.utils import isunicode


class TestIsUnicodeString(object):
    """Test class for testing the isunicode function.
    """

    def test_isunicode_none(self):
        """Test that None is not a unicdoe string.
        """

        assert not isunicode(None)

    def test_isunicode_int(self):
        """Test that int (a primitive type) is not a unicode string.
        """

        assert not isunicode(0)

    def test_isunicode_list(self):
        """Test that a list (a Python object) is not a unicode string.
        """

        assert not isunicode(['hello', 'world'])

    def test_isunicode_byte(self):
        """Test that an explicit byte string is not a Unicode string.
        """

        assert not isunicode(b'Hello, world!')

    def test_isunicode_str(self):
        """Test that the default string type in Python 3 is a unicode string
        but not in Python 2.
        """

        # In Python 3 strings are unicode encoded by default.
        if six.PY3:
            assert isunicode('Hello, world!')
        else:
            assert not isunicode('Hello, world!')

    def test_isunicode_unicode(self):
        """Test that a unicode literal is a unicode string.
        """

        assert isunicode(u'Hello, world!')
