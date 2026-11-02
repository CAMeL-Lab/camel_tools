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
Tests for camel_tools.morphology.utils
"""

from types import SimpleNamespace

from camel_tools.morphology.utils import merge_features


_DB = SimpleNamespace(defines={}, compute_feats=frozenset())


class TestMergeFeatures(object):
    """Test class for testing the merge_features function.
    """

    def test_affix_source_does_not_overwrite_stem_source(self):
        """Test that the stem keeps its source when the affixes have one.
        """

        merged = merge_features(_DB, {'source': 'lex'},
                                {'diac': 'a', 'source': 'wiki'},
                                {'source': 'lex'})

        assert merged['source'] == 'wiki'

    def test_affix_feature_overwrites_stem_feature(self):
        """Test that affix values still replace other stem features.
        """

        merged = merge_features(_DB, {'gen': '-'},
                                {'diac': 'a', 'gen': 'm', 'num': 's'},
                                {'gen': 'f', 'num': ''})

        assert merged['gen'] == 'f'
        assert merged['num'] == 's'
