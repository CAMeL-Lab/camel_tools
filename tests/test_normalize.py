# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2019 New York University Abu Dhabi
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
Tests for camel_tools.utils.normalize
"""


from camel_tools.utils.normalize import remove_elongation_ar


class TestElongationRemoval(object):
    """Test class for the elongation removal functions
    """

    def test_remove_elongation_ar_empty_str(self):
    	"""Test that an empty string will return an empty string
    	"""

    	assert remove_elongation_ar('') == ''


    def test_remove_elongation_ar_no_dups(self):
    	"""Test that two consecutive duplicates will not be removed
    	from the string.
    	"""

    	assert remove_elongation_ar('\u0645\u0645\u064a\u0632') == '\u0645\u0645\u064a\u0632'


    def test_remove_elongation_ar_start(self):
    	"""Test that more than two consecutive duplicates at the beginning
    	will be removed from the string.
    	"""

    	assert remove_elongation_ar('\u0643\u0643\u0643\u062a\u064a\u0631') == '\u0643\u062a\u064a\u0631'


    def test_remove_elongation_ar_middle(self):
    	"""Test that more than two consecutive duplicates at the middle
    	will be removed from the string.
    	"""

    	assert remove_elongation_ar('\u0643\u062a\u064a\u064a\u064a\u0631') == '\u0643\u062a\u064a\u0631'


    def test_remove_elongation_ar_end(self):
    	"""Test that more than two consecutive duplicates at the end
    	will be removed from the string.
    	"""

    	assert remove_elongation_ar('\u0643\u062a\u064a\u0631\u0631\u0631') == '\u0643\u062a\u064a\u0631'
