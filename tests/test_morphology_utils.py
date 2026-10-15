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

"""Tests for camel_tools.morphology.utils."""

from camel_tools.morphology.utils import rewrite_caphi


class TestRewriteCaphi(object):

    def test_iy_uw_no_suffix(self):
        # Issue #138: stem-final i_y / u_w with no suffix (qaaDiy, yad3uw)
        assert rewrite_caphi('q_aa_d._i_y-') == 'q_aa_d._ii'
        assert rewrite_caphi('y_a_d_3_u_w-') == 'y_a_d_3_uu'

    def test_iy_uw_consonant_suffix(self):
        assert rewrite_caphi('q_aa_d._i_y-+t_u') == 'q_aa_d._ii_t_u'
        assert rewrite_caphi('y_a_d_3_u_w-+n_a') == 'y_a_d_3_uu_n_a'

    def test_iy_uw_vowel_suffix_unchanged(self):
        assert rewrite_caphi('q_aa_d._i_y-+a') == 'q_aa_d._i_y_a'
        assert rewrite_caphi('q_aa_d._i_y-+aa') == 'q_aa_d._i_y_aa'
        assert rewrite_caphi('y_a_d_3_u_w-+a') == 'y_a_d_3_u_w_a'

    def test_iy_uw_with_prefix_and_multiple_suffixes(self):
        assert rewrite_caphi('w_a_+q_aa_d._i_y-') == 'w_a_q_aa_d._ii'
        assert rewrite_caphi('q_aa_d._i_y-+t_u+h_aa') == 'q_aa_d._ii_t_u_h_aa'
        assert rewrite_caphi('q_aa_d._i_y-+a+h_aa') == 'q_aa_d._i_y_a_h_aa'

    def test_iy_uw_inside_stem_untouched(self):
        assert rewrite_caphi('b_i_y_t-+u') == 'b_i_y_t_u'
