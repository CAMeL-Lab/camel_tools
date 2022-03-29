# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2022 New York University Abu Dhabi
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
Tests for camel_tools.transliterate.
"""

from __future__ import absolute_import

import pytest

from camel_tools.utils.charmap import CharMapper
from camel_tools.utils.transliterate import Transliterator


# A mapper that translates lower-case English characters to a lower-case x and
# upper-case English characters to an upper-case X. This makes it easy to
# predict what the transliteration should be.
TEST_MAP = {
    u'A-Z': u'X',
    u'a-z': u'x',
}
TEST_MAPPER = CharMapper(TEST_MAP, None)


class TestTransliteratorInit(object):
    """Test class for Transliterator.__init__.
    """

    def test_init_none_mapper(self):
        """Test that init raises a TypeError when given a mapper that is None.
        """

        with pytest.raises(TypeError):
            Transliterator(None)

    def test_init_invalid_type_mapper(self):
        """Test that init raises a TypeError when given a mapper that is not a
        CharMapper instance.
        """

        with pytest.raises(TypeError):
            Transliterator({})

    def test_init_valid_mapper(self):
        """Test that init doesn't raise an error when given a valid mapper.
        """

        assert Transliterator(TEST_MAPPER)

    def test_init_none_marker(self):
        """Test that init raises a TypeError when given a marker that is None.
        """

        with pytest.raises(TypeError):
            Transliterator(TEST_MAPPER, None)

    def test_init_invalid_type_marker(self):
        """Test that init raises a TypeError when given a marker that is not a
        string.
        """

        with pytest.raises(TypeError):
            Transliterator(TEST_MAPPER, [])

    def test_init_empty_marker(self):
        """Test that init raises a ValueError when given a marker that is an
        empty string.
        """

        with pytest.raises(ValueError):
            Transliterator(TEST_MAPPER, '')

    def test_init_invalid_marker1(self):
        """Test that init raises a ValueError when given an invalid marker (
        wgitespace in the middle).
        """

        with pytest.raises(ValueError):
            Transliterator(TEST_MAPPER, '@@LAT @@')

    def test_init_invalid_marker2(self):
        """Test that init raises a ValueError when given an invalid marker (
        whitespace at the end).
        """

        with pytest.raises(ValueError):
            Transliterator(TEST_MAPPER, '@@LAT@@ ')

    def test_init_invalid_marker3(self):
        """Test that init raises a ValueError when given an invalid marker (
        whitespace at the beginning).
        """

        with pytest.raises(ValueError):
            Transliterator(TEST_MAPPER, ' @@LAT@@')

    def test_init_valid_marker1(self):
        """Test that init doesn't raise an error when given a valid marker.
        """

        assert Transliterator(TEST_MAPPER, '@@LAT@@')

    def test_init_valid_marker2(self):
        """Test that init doesn't raise an error when given a valid marker.
        """

        assert Transliterator(TEST_MAPPER, u'@@LAT@@')


class TestTransliteratorTranslate(object):
    """Test class for Transliterator.translate.
    """

    def test_trans_empty(self):
        """Test that transliterating an empty string returns an empty string.
        """

        trans = Transliterator(TEST_MAPPER, '@@')
        assert trans.transliterate(u'') == u''

    def test_trans_single_no_markers(self):
        """Test that a single word with no markers gets transliterated.
        """

        trans = Transliterator(TEST_MAPPER, '@@')
        assert trans.transliterate(u'Hello') == u'Xxxxx'

    def test_trans_single_with_markers(self):
        """Test that a single word with markers does not get transliterated.
        """

        trans = Transliterator(TEST_MAPPER, '@@')
        assert trans.transliterate(u'@@Hello') == u'@@Hello'

    def test_trans_single_strip(self):
        """Test that a single word with markers does not get transliterated
        but markers do get stripped when strip_markers is set to True.
        """

        trans = Transliterator(TEST_MAPPER, '@@')
        assert trans.transliterate(u'@@Hello', True) == u'Hello'

    def test_trans_single_ignore(self):
        """Test that a single word with markers gets transliterated when ignore
        markers is set to True.
        """

        trans = Transliterator(TEST_MAPPER, '@@')
        assert trans.transliterate(u'@@Hello', False, True) == u'@@Xxxxx'

    def test_trans_single_ignore_strip(self):
        """Test that a single word with markers gets transliterated with
        markers stripped when both strip_markers and ignore_markers are set to
        True.
        """

        trans = Transliterator(TEST_MAPPER, '@@')
        assert trans.transliterate(u'@@Hello', True, True) == u'Xxxxx'

    def test_trans_sent_no_markers(self):
        """Test that a sentence with no markers gets transliterated.
        """

        sent_orig = u'Hello World, this is a sentence!'
        sent_out = u'Xxxxx Xxxxx, xxxx xx x xxxxxxxx!'

        trans = Transliterator(TEST_MAPPER, '@@')
        assert trans.transliterate(sent_orig) == sent_out

    def test_trans_sent_with_markers(self):
        """Test that tokens with markers in a sentence do not get
        transliterated.
        """

        sent_orig = u'Hello @@World, this is a @@sentence!'
        sent_out = u'Xxxxx @@World, xxxx xx x @@sentence!'

        trans = Transliterator(TEST_MAPPER, '@@')
        assert trans.transliterate(sent_orig) == sent_out

    def test_trans_sent_strip(self):
        """Test that tokens with markers in a sentence do not get
        transliterated but markers do get stripped when strip_markers is set
        to True.
        """

        sent_orig = u'Hello @@World, this is a @@sentence!'
        sent_out = u'Xxxxx World, xxxx xx x sentence!'

        trans = Transliterator(TEST_MAPPER, '@@')
        assert trans.transliterate(sent_orig, True) == sent_out

    def test_trans_sent_ignore(self):
        """Test that tokens with markers in a sentence get transliterated
        when ignore markers is set to True.
        """

        sent_orig = u'Hello @@World, this is a @@sentence!'
        sent_out = u'Xxxxx @@Xxxxx, xxxx xx x @@xxxxxxxx!'

        trans = Transliterator(TEST_MAPPER, '@@')
        assert trans.transliterate(sent_orig, False, True) == sent_out

    def test_trans_sent_ignore_strip(self):
        """Test that tokens with markers in a sentence get transliterated with
        markers stripped when both strip_markers and ignore_markers are set to
        True.
        """

        sent_orig = u'Hello @@World, this is a @@sentence!'
        sent_out = u'Xxxxx Xxxxx, xxxx xx x xxxxxxxx!'

        trans = Transliterator(TEST_MAPPER, '@@')
        assert trans.transliterate(sent_orig, True, True) == sent_out
