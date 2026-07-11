# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2026 New York University Abu Dhabi
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
Tests for camel_tools.utils.dediac
"""

from camel_tools.utils.dediac import dediac_ar, dediac_bw, dediac_safebw
from camel_tools.utils.dediac import dediac_xmlbw, dediac_hsb


class TestDediacAr(object):
    """Test class for dediac_ar.
    """

    def test_dediac_ar_empty(self):
        assert dediac_ar(u'') == u''

    def test_dediac_ar_removes_harakat(self):
        # muHamamd with kasra/fatha/shadda/damma -> bare letters
        assert dediac_ar(u'مُحَمَّد'
                         u'ٌ') == u'محمد'

    def test_dediac_ar_keeps_alef_wasla(self):
        # dagger alef removed, alef-wasla (a letter) kept
        assert dediac_ar(u'ٱلَم') == \
            u'ٱلم'


class TestDediacBw(object):
    """Test class for dediac_bw.
    """

    def test_dediac_bw_empty(self):
        assert dediac_bw(u'') == u''

    def test_dediac_bw_removes_harakat(self):
        assert dediac_bw(u'muHam~ada') == u'mHmd'


class TestDediacHsb(object):
    """Test class for dediac_hsb.
    """

    def test_dediac_hsb_empty(self):
        assert dediac_hsb(u'') == u''

    def test_dediac_hsb_removes_harakat(self):
        # fatha 'a' is a diacritic and should be removed
        assert dediac_hsb(u'Äalm') == u'Älm'

    def test_dediac_hsb_keeps_alef_wasla(self):
        # Alef-Wasla (Ä in HSB) is a letter, it must NOT be stripped
        assert u'Ä' in dediac_hsb(u'Äalm')
