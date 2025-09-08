# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2025 New York University Abu Dhabi
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

"""Utility functions used by the various morphology components.
"""

import copy
import re
import sys


# eatures which should be concatinated when generating analysis
_JOIN_FEATS = frozenset(['gloss', 'bw'])
_CONCAT_FEATS = frozenset(['diac', 'pattern', 'caphi', 'catib6', 'ud'])
_CONCAT_FEATS_NONE = frozenset(['d3tok', 'd3seg', 'atbseg', 'd2seg', 'd1seg',
                                'd1tok', 'd2tok', 'atbtok', 'bwtok'])
_LOGPROB_FEATS = frozenset(['pos_logprob', 'lex_logprob', 'pos_lex_logprob'])

# Tokenization and segmentation schemes to which Sun letters and Fatha after 
# Alif rewrite rules apply
_TOK_SCHEMES_1 = frozenset(['d1tok', 'd2tok', 'atbtok', 'd1seg', 'd2seg',
                            'd3seg', 'atbseg'])
# Tokenization and segmentation schemes to which only the Fatha after Alif 
# rewrite rule apply
_TOK_SCHEMES_2 = frozenset(['d3tok', 'd3seg'])

# Splits lemmas on '_' and '-'
_STRIP_LEX_RE = re.compile('_|-')

# Sun letters with definite article
_REWRITE_DIAC_RE_1 = re.compile(u'#\\+*([\u062a\u062b\u062f\u0630\u0631\u0632'
                                u'\u0633\u0634\u0635\u0636\u0637\u0638\u0644'
                                u'\u0646])')
# Moon letters with definite article
_REWRITE_DIAC_RE_2 = re.compile(u'#\\+*')
# Fatha after Alif
_REWRITE_DIAC_RE_3 = re.compile(u'\u0627\\+?\u064e([\u0629\u062a])')
# Hamza Wasl
_REWRITE_DIAC_RE_4 = re.compile(u'\u0671')
# Remove '+'s
_REWRITE_DIAC_RE_5 = re.compile(u'\\+')
# Fix Multiple Shadda's
# FIXME: Remove after DB fix
_REWRITE_DIAC_RE_6 = re.compile(u'\u0651+')

# Sun letters
_REWRITE_CAPHI_RE_1 = re.compile(u'(l-)\\+(t\\_|th\\_|d\\_|th\\.\\_|r\\_|z\\_|'
                                 u's\\_|sh\\_|s\\.\\_|d\\.\\_|t\\.\\_|'
                                 u'dh\\.\\_|l\\_|n\\_|dh\\_)')
# Replace shadda
_REWRITE_CAPHI_RE_2 = re.compile(u'(\\S)[-]*\\+~')
# Replace ending i_y with ii if suffix is not a vowel
_REWRITE_CAPHI_RE_3 = re.compile(u'i\\_y-\\+([^iau]+|$)')
# Replacing ending u_w with uu if suffix is not a vowel
_REWRITE_CAPHI_RE_4 = re.compile(u'u\\_w-\\+([^iau]+|$)')
# Remove hamza wasl if preceeded by a vowel
_REWRITE_CAPHI_RE_5 = re.compile(u'([iua])\\+-2_[iua]')
# Remove hamza wasl if preceeded by a non-vowel
_REWRITE_CAPHI_RE_6 = re.compile(u'(.+)\\+-2_([iua])')
# Handle _u+w_ cases followed by non-vowels (eg. 2_u+w_l_ii)
_REWRITE_CAPHI_RE_7 = re.compile(u'u\\+w(_+[^ioua])')
# Handle stems followed that end with taa marboutah
_REWRITE_CAPHI_RE_8 = re.compile(u'p-\\+([iua])')
# Compress alef madda followed by fatha followed by short vowels
_REWRITE_CAPHI_RE_9 = re.compile(u'aa\\+a[_]*')
# Remove '+'s
_REWRITE_CAPHI_RE_10 = re.compile(u'[\\+-]')
# Remove multiple '_'
_REWRITE_CAPHI_RE_11 = re.compile(u'_+')
# Remove initial and tailing underscores tailing taa marboutah
_REWRITE_CAPHI_RE_12 = re.compile(u'((^\\_+)|(\\_p?\\_*$))')

# Normalize tanwyn
_NORMALIZE_TANWYN_FA_RE = re.compile(u'\u064b\u0627')
_NORMALIZE_TANWYN_FY_RE = re.compile(u'\u064b\u0649')
_NORMALIZE_TANWYN_AF_RE = re.compile(u'\u0627\u064b')
_NORMALIZE_TANWYN_YF_RE = re.compile(u'\u0649\u064b')

# Simple Arabic script to CAPHI map
_AR2CAPHI = {
        '\u0621': '2',
        '\u0622': '2_aa',
        '\u0623': '2',
        '\u0624': '2',
        '\u0625': '2',
        '\u0626': '2',
        '\u0627': 'aa',
        '\u0628': 'b',
        '\u062A': 't',
        '\u062B': 'th',
        '\u062C': 'j',
        '\u062D': '7',
        '\u062E': 'kh',
        '\u062F': 'd',
        '\u0630': 'dh',
        '\u0631': 'r',
        '\u0632': 'z',
        '\u0633': 's',
        '\u0634': 'sh',
        '\u0635': 's.',
        '\u0636': 'd.',
        '\u0637': 't.',
        '\u0638': 'dh.',
        '\u0639': '3',
        '\u063A': 'gh',
        '\u0641': 'f',
        '\u0642': 'q',
        '\u0643': 'k',
        '\u0644': 'l',
        '\u0645': 'm',
        '\u0646': 'n',
        '\u0647': 'h',
        '\u0648': 'w',
        '\u0649': 'aa',
        '\u064A': 'y'
}


def strip_lex(lex):
    return _STRIP_LEX_RE.split(lex)[0]


def simple_ar_to_caphi(ar_str):
    """Convert Arabic script to CAPHI.
    Args:
        ar_str (:obj:`str`): String to convert.
    Returns:
        :obj:`str`: CAPHI string.
    """
    # If the first letter is Alif change it to hamza Alif to map it to '2'
    if ar_str.startswith('\u0627'):
        ar_str = '\u0623{}'.format(ar_str[1:])

    return '_'.join([_AR2CAPHI[x] for x in ar_str if x in _AR2CAPHI])


def normalize_tanwyn(word, mode='AF'):
    if mode == 'FA':
        word = _NORMALIZE_TANWYN_FA_RE.sub(u'\u064b\u0627', word)
        word = _NORMALIZE_TANWYN_FY_RE.sub(u'\u064b\u0649', word)
    else:
        word = _NORMALIZE_TANWYN_AF_RE.sub(u'\u0627\u064b', word)
        word = _NORMALIZE_TANWYN_YF_RE.sub(u'\u0649\u064b', word)
    return word


def rewrite_diac(word):
    word = _REWRITE_DIAC_RE_1.sub(u'\\1\u0651', word)
    word = _REWRITE_DIAC_RE_2.sub(u'', word)
    word = _REWRITE_DIAC_RE_3.sub(u'\u0627\\1', word)
    word = _REWRITE_DIAC_RE_4.sub(u'\u0627', word)
    word = _REWRITE_DIAC_RE_5.sub(u'', word)
    word = _REWRITE_DIAC_RE_6.sub(u'\u0651', word)

    return word


def rewrite_caphi(word):
    word = _REWRITE_CAPHI_RE_1.sub(u'\\2\\2', word)
    word = _REWRITE_CAPHI_RE_2.sub(u'\\1_\\1', word)
    word = _REWRITE_CAPHI_RE_3.sub(u'ii_\\1', word)
    word = _REWRITE_CAPHI_RE_4.sub(u'uu_\\1', word)
    word = _REWRITE_CAPHI_RE_5.sub(u'\\1', word)
    word = _REWRITE_CAPHI_RE_6.sub(u'\\1_\\2', word)
    word = _REWRITE_CAPHI_RE_7.sub(u'uu\\1', word)
    word = _REWRITE_CAPHI_RE_8.sub(u't_\\1', word)
    word = _REWRITE_CAPHI_RE_9.sub(u'aa_', word)
    word = _REWRITE_CAPHI_RE_10.sub(u'_', word)
    word = _REWRITE_CAPHI_RE_11.sub(u'_', word)
    word = _REWRITE_CAPHI_RE_12.sub(u'', word)

    return word


def rewrite_tok_1(word):
    word = _REWRITE_DIAC_RE_1.sub(u'\\1\u0651', word)
    word = _REWRITE_DIAC_RE_2.sub(u'', word)
    word = _REWRITE_DIAC_RE_3.sub(u'\u0627\\1', word)

    return word


def rewrite_tok_2(word):
    word = _REWRITE_DIAC_RE_3.sub(u'\u0627\\1', word)

    return word


def rewrite_pattern(word):
    word = _REWRITE_DIAC_RE_2.sub(u'', word)

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

    for join_feat in _JOIN_FEATS:
        if join_feat in db.defines:
            feat_vals = [
                prefix_feats.get(join_feat, None),
                stem_feats.get(join_feat, None),
                suffix_feats.get(join_feat, None)
            ]
            result[join_feat] = u'+'.join([fv for fv in feat_vals
                                           if fv is not None and fv != ''])

    for concat_feat in _CONCAT_FEATS:
        if concat_feat in db.defines:
            result[concat_feat] = u'+'.join([x for x in [
                prefix_feats.get(concat_feat, ''),
                stem_feats.get(concat_feat, ''),
                suffix_feats.get(concat_feat, '')] if len(x) > 0])

    for concat_feat in _CONCAT_FEATS_NONE:
        if concat_feat in db.defines:
            result[concat_feat] = u'{}{}{}'.format(
                prefix_feats.get(concat_feat, ''),
                stem_feats.get(concat_feat, stem_feats.get('diac', '')),
                suffix_feats.get(concat_feat, ''))

    result['stem'] = stem_feats['diac']
    result['stemgloss'] = stem_feats.get('gloss', '')

    result['diac'] = normalize_tanwyn(rewrite_diac(result['diac']),
                                      diac_mode)

    for feat in _TOK_SCHEMES_1:
        if feat in db.defines:
            result[feat] = rewrite_tok_1(result.get(feat, ''))

    for feat in _TOK_SCHEMES_2:
        if feat in db.defines:
            result[feat] = rewrite_tok_2(result.get(feat, ''))

    if 'caphi' in db.defines:
        result['caphi'] = rewrite_caphi(result.get('caphi', ''))

    if 'form_gen' in db.defines and result['gen'] == '-':
        result['gen'] = result['form_gen']

    if 'form_num' in db.defines and result['num'] == '-':
        result['num'] = result['form_num']

    if 'pattern' in db.compute_feats:
        result['pattern'] = u'{}{}{}'.format(prefix_feats.get('diac', ''),
                                             stem_feats.get('pattern',
                                             stem_feats.get('diac', '')),
                                             suffix_feats.get('diac', ''))
        result['pattern'] = rewrite_pattern(result['pattern'])

    for logprob_feat in _LOGPROB_FEATS:
        if logprob_feat in db.defines:
            result[logprob_feat] = float(result.get(logprob_feat, -99.0))

    return result


def feat_prettyprint(feats, order, default='', file=sys.stdout):
    for feat in order:
        feat_value = repr(feats.get(feat, default))
        print(f'{feat}: {feat_value}', file=file)
