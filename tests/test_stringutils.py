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
Tests for camel_tools.utils.stringutils
"""

from camel_tools.utils.stringutils import isunicode


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

        assert isunicode('Hello, world!')

    def test_isunicode_unicode(self):
        """Test that a unicode literal is a unicode string.
        """

        assert isunicode(u'Hello, world!')
