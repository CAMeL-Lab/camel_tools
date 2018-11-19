# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018 New York University Abu Dhabi
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

"""Utility functions used by the various components of Calima Star.
"""

import copy
import regex as re

# features which should be concatinated when generating analysis
_CONCAT_FEATS = ['diac', 'bw', 'gloss', 'pattern', 'caphi', 'catib6', 'ud']
_CONCAT_FEATS_NONE = ['d3tok', 'd3seg', 'atbseg', 'd2seg', 'd1seg', 'd1tok',
                      'd2tok', 'atbtok']  # FIXME: DON'T DO THIS!!!!!

# Sun letters
_REWRITE_DIAC_RE_1 = re.compile(r'^((وَ|فَ)?(بِ|كَ)?ال)\+?([تثدذرزسشصضطظلن])')
# Sun letters
_REWRITE_DIAC_RE_2 = re.compile(r'^((وَ|فَ)?لِل)\+?([تثدذرزسشصضطظلن])')
# Fatha after Alif
_REWRITE_DIAC_RE_3 = re.compile(r'ا\+?َ([ةت])')
# Hamza Wasl
_REWRITE_DIAC_RE_4 = re.compile(r'ٱ')
# Remove '+'s
_REWRITE_DIAC_RE_5 = re.compile(r'\+')
# Fix Multiple Shadda's
# FIXME: Remove after DB fix
_REWRITE_DIAC_RE_6 = re.compile(r'ّ+')

# Sun letters
_REWRITE_CAPHI_RE_1 = re.compile(r'^((w\_a\_|f\_a\_|2\_a\_)?'
                                 r'(b\_i\_|k\_a\_|l\_i\_)?l)\+'
                                 r'(t\_|th\_|d\_|th\.\_|r\_|z\_|s\_|sh\_|'
                                 r's\.\_|d\.\_|t\.\_|dh\.\_|l\_|n\_|dh\_)')
# Replace shadda
_REWRITE_CAPHI_RE_2 = re.compile(r'(\S)\+~')
# Remove '+'s
_REWRITE_CAPHI_RE_3 = re.compile(r'\+')
# Remove initial and tailing underscores
_REWRITE_CAPHI_RE_4 = re.compile(r'(^\_|\_$)')

# Normalize tanwyn
_NORMALIZE_TANWYN_FA_RE = re.compile(r'ًا')
_NORMALIZE_TANWYN_FY_RE = re.compile(r'ًى')
_NORMALIZE_TANWYN_AF_RE = re.compile(r'اً')
_NORMALIZE_TANWYN_YF_RE = re.compile(r'ىً')


def normalize_tanwyn(word, mode='AF'):
    if mode == 'FA':
        word = _NORMALIZE_TANWYN_FA_RE.sub('ًا', word)
        word = _NORMALIZE_TANWYN_FY_RE.sub('ًى', word)
    else:
        word = _NORMALIZE_TANWYN_AF_RE.sub('اً', word)
        word = _NORMALIZE_TANWYN_YF_RE.sub('ىً', word)
    return word


def rewrite_diac(word):
    word = _REWRITE_DIAC_RE_1.sub(r'\1\4ّ', word)
    word = _REWRITE_DIAC_RE_2.sub(r'\1\3ّ', word)
    word = _REWRITE_DIAC_RE_3.sub(r'ا\1', word)
    word = _REWRITE_DIAC_RE_4.sub(r'ا', word)
    word = _REWRITE_DIAC_RE_5.sub(r'', word)
    word = _REWRITE_DIAC_RE_6.sub(r'ّ', word)

    return word


def rewrite_caphi(word):
    word = _REWRITE_CAPHI_RE_1.sub(r'\2\3\4\4', word)
    word = _REWRITE_CAPHI_RE_2.sub(r'\1_\1', word)
    word = _REWRITE_CAPHI_RE_3.sub(r'_', word)
    word = _REWRITE_CAPHI_RE_4.sub('', word)
    return word


def merge_features(db, prefix_feats, stem_feats, suffix_feats, diac_mode="AF"):
    result = copy.copy(stem_feats)

    for stem_feat in stem_feats:
        suffix_feat_val = suffix_feats.get(stem_feat, '')
        if suffix_feat_val != '-' and suffix_feat_val != '':
            result[stem_feat] = suffix_feat_val

        prefix_feat_val = prefix_feats.get(stem_feat, '')
        if prefix_feat_val != '-' and prefix_feat_val != '':
            result[stem_feat] = prefix_feat_val

    for concat_feat in _CONCAT_FEATS:
        result[concat_feat] = '{}+{}+{}'.format(
            prefix_feats.get(concat_feat, ''),
            stem_feats.get(concat_feat, ''),
            suffix_feats.get(concat_feat, ''))

    for concat_feat in _CONCAT_FEATS_NONE:
        result[concat_feat] = '{}{}{}'.format(
            prefix_feats.get(concat_feat, ''),
            stem_feats.get(concat_feat, ''),
            suffix_feats.get(concat_feat, ''))

    result['stem'] = stem_feats['diac']
    result['stemgloss'] = stem_feats.get('gloss', '')
    result['diac'] = normalize_tanwyn(rewrite_diac(result['diac']),
                                      diac_mode)
    result['caphi'] = rewrite_caphi(result.get('caphi', ''))

    if result['gen'] == '-':
        result['gen'] = result['form_gen']

    if result['num'] == '-':
        result['num'] = result['form_num']

    if 'pattern' in db.compute_feats:
        result['pattern'] = '{}{}{}'.format(prefix_feats.get('diac', ''),
                                            stem_feats['pattern'],
                                            suffix_feats.get('diac', ''))

    return result
