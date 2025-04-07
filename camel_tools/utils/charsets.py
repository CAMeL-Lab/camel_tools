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

"""Contains character sets for different encoding schemes as well as Unicode
characters marked as symbols and punctuation.
"""

import unicodedata

from emoji import EMOJI_DATA


__all__ = (
    'UNICODE_PUNCT_CHARSET',
    'UNICODE_SYMBOL_CHARSET',
    'UNICODE_LETTER_CHARSET',
    'UNICODE_MARK_CHARSET',
    'UNICODE_NUMBER_CHARSET',
    'UNICODE_PUNCT_SYMBOL_CHARSET',
    'UNICODE_LETTER_MARK_NUMBER_CHARSET',
    'EMOJI_ALL_CHARSET',
    'EMOJI_SINGLECHAR_CHARSET',
    'EMOJI_MULTICHAR_CHARSET', 
    'AR_LETTERS_CHARSET',
    'AR_DIAC_CHARSET',
    'AR_CHARSET',
    'BW_LETTERS_CHARSET',
    'BW_DIAC_CHARSET',
    'BW_CHARSET',
    'SAFEBW_LETTERS_CHARSET',
    'SAFEBW_DIAC_CHARSET',
    'SAFEBW_CHARSET',
    'XMLBW_LETTERS_CHARSET',
    'XMLBW_DIAC_CHARSET',
    'XMLBW_CHARSET',
    'HSB_LETTERS_CHARSET',
    'HSB_DIAC_CHARSET',
    'HSB_CHARSET',
)


# Precompute Unicode charsets
_UNICODE_PUNCT_CHARSET = set()
_UNICODE_SYMBOL_CHARSET = set()
_UNICODE_LETTER_CHARSET = set()
_UNICODE_MARK_CHARSET = set()
_UNICODE_NUMBER_CHARSET = set()

for x in range(0x110000):
    x_chr = chr(x)
    x_cat = unicodedata.category(x_chr)

    if x_cat[0] == 'L':
        _UNICODE_LETTER_CHARSET.add(x_chr)
    elif x_cat[0] == 'M':
        _UNICODE_MARK_CHARSET.add(x_chr)
    elif x_cat[0] == 'N':
        _UNICODE_NUMBER_CHARSET.add(x_chr)
    elif x_cat[0] == 'P':
        _UNICODE_PUNCT_CHARSET.add(x_chr)
    elif x_cat[0] == 'S':
        _UNICODE_SYMBOL_CHARSET.add(x_chr)


UNICODE_PUNCT_CHARSET: frozenset[str] = frozenset(_UNICODE_PUNCT_CHARSET)
"""A set of all Unicode characters marked as punctuation."""

UNICODE_SYMBOL_CHARSET: frozenset[str] = frozenset(_UNICODE_SYMBOL_CHARSET)
"""A set of all Unicode characters marked as symbols."""

UNICODE_LETTER_CHARSET: frozenset[str] = frozenset(_UNICODE_LETTER_CHARSET)
""""""

UNICODE_MARK_CHARSET: frozenset[str] = frozenset(_UNICODE_MARK_CHARSET)
""""""

UNICODE_NUMBER_CHARSET: frozenset[str] = frozenset(_UNICODE_NUMBER_CHARSET)
""""""

UNICODE_PUNCT_SYMBOL_CHARSET: frozenset[str] = (
    UNICODE_PUNCT_CHARSET | UNICODE_SYMBOL_CHARSET)
"""A set of all Unicode characters marked as either punctuation or symbol."""

UNICODE_LETTER_MARK_NUMBER_CHARSET: frozenset[str] = (
    UNICODE_LETTER_CHARSET |
    UNICODE_MARK_CHARSET |
    UNICODE_NUMBER_CHARSET)
""""""


# Delete temporary charsets
# TODO: Is this neccessary?
del _UNICODE_LETTER_CHARSET
del _UNICODE_MARK_CHARSET
del _UNICODE_NUMBER_CHARSET
del _UNICODE_SYMBOL_CHARSET
del _UNICODE_PUNCT_CHARSET


EMOJI_ALL_CHARSET: frozenset[str] = frozenset(EMOJI_DATA.keys())
"""A set of all emojis (union of :obj:`EMOJI_SINGLECHAR_CHARSET` and
:obj:`EMOJI_MULTICHAR_CHARSET`)."""

EMOJI_SINGLECHAR_CHARSET: frozenset[str] = frozenset([
    x for x in EMOJI_ALL_CHARSET if len(x) == 1])
"""A set of all single-character emojis."""

EMOJI_MULTICHAR_CHARSET: frozenset[str] = frozenset([
    x for x in EMOJI_ALL_CHARSET if len(x) > 1])
"""A set of all multi-character emojis."""

AR_LETTERS_CHARSET: frozenset[str] = frozenset(
    '\u0621\u0622\u0623\u0624\u0625\u0626\u0627\u0628\u0629\u062a\u062b\u062c\u062d\u062e\u062f'
    '\u0630\u0631\u0632\u0633\u0634\u0635\u0636\u0637\u0638\u0639\u063a\u0640\u0641\u0642\u0643'
    '\u0644\u0645\u0646\u0647\u0648\u0649\u064a\u0671\u067e\u0686\u06a4\u06af')
"""A set of all Unicode Arabic letters."""

AR_DIAC_CHARSET: frozenset[str] = frozenset(
    '\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0670')
"""A set of all Unicode Arabic diacritics."""

AR_CHARSET: frozenset[str] = AR_LETTERS_CHARSET | AR_DIAC_CHARSET
"""A set of all Unicode Arabic letters and diacritics."""

BW_LETTERS_CHARSET: frozenset[str] = frozenset('$&\'*<>ADEGHJPSTVYZ_bdfghjklmnpqrstvwxyz{|}_')
"""A set of all Arabic letters in Buckwalter encoding."""

BW_DIAC_CHARSET: frozenset[str] = frozenset('FKN`aiou~')
"""A set of all Arabic diacritics in Buckwalter encoding."""

BW_CHARSET: frozenset[str] = BW_LETTERS_CHARSET | BW_DIAC_CHARSET
"""A set of all Arabic letters and diacritics in Buckwalter encoding."""

SAFEBW_LETTERS_CHARSET: frozenset[str] = frozenset('ABCDEGHIJLMOPQSTVWYZ_bcdefghjklmnpqrstvwxyz')
"""A set of all Arabic letters in Safe Buckwalter encoding."""

SAFEBW_DIAC_CHARSET: frozenset[str] = frozenset('FKNaeiou~')
"""A set of all Arabic diacritics in Safe Buckwalter encoding."""

SAFEBW_CHARSET: frozenset[str] = SAFEBW_LETTERS_CHARSET | SAFEBW_DIAC_CHARSET
"""A set of all Arabic letters and diacritics in Safe Buckwalter encoding."""

XMLBW_LETTERS_CHARSET: frozenset[str] = frozenset('$\'*ABDEGHIJOPSTWYZ_bdfghjklmnpqrstvwxyz{|}')
"""A set of all Arabic letters in XML Buckwalter encoding."""

XMLBW_DIAC_CHARSET: frozenset[str] = frozenset('FKN`aiou~')
"""A set of all Arabic diacritics in XML Buckwalter encoding."""

XMLBW_CHARSET: frozenset[str] = XMLBW_LETTERS_CHARSET | XMLBW_DIAC_CHARSET
"""A set of all Arabic letters and diacritics in XML Buckwalter encoding."""

HSB_LETTERS_CHARSET: frozenset[str] = frozenset(
    '\'ADHST_bcdfghjklmnpqrstvwxyz\u00c2\u00c4\u00e1\u00f0\u00fd\u0100\u0102\u010e\u0127\u0161'
    '\u0175\u0177\u03b3\u03b8\u03c2')
"""A set of all Arabic letters in Habash-Soudi-Buckwalter encoding."""

HSB_DIAC_CHARSET: frozenset[str] = frozenset('.aiu~\u00c4\u00e1\u00e3\u0129\u0169')
"""A set of all Arabic diacritics in Habash-Soudi-Buckwalter encoding."""

HSB_CHARSET: frozenset[str] = HSB_LETTERS_CHARSET | HSB_DIAC_CHARSET
"""A set of all Arabic letters and diacritics in Habash-Soudi-Buckwalter encoding."""
