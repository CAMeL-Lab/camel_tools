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

"""Contains character sets for different encoding schemes as well as Unicode
characters marked as symbols and punctuation.
"""

import unicodedata

from six import unichr


UNICODE_PUNCT_CHARSET = frozenset(
    [unichr(x) for x in range(65536) if unicodedata.category(
        unichr(x))[0] == 'P'])
UNICODE_SYMBOL_CHARSET = frozenset(
    [unichr(x) for x in range(65536) if unicodedata.category(
        unichr(x))[0] == 'S'])
UNICODE_PUNCT_SYMBOL_CHARSET = UNICODE_PUNCT_CHARSET | UNICODE_SYMBOL_CHARSET

AR_CHARSET = frozenset(u'ءآأؤإئابةتثجحخدذرزسشصضطظعغـفقكلمنهوىيًٌٍَُِّْٰٱپڤگءآ'
                       u'أؤإئابةتثجحخدذرزسشصضطظعغـفقكلمنهوىيًٌٍَُِّْٰٱپچڤگ')
AR_LETTERS_CHARSET = frozenset(u'ءآأؤإئابةتثجحخدذرزسشصضطظعغـفقكلمنهوىيٱپچڤگ')
AR_DIAC_CHARSET = frozenset(u'ًٌٍَُِّْٰ')

BW_CHARSET = frozenset(u'$&\'*<>ADEFGHJKNPSTVYZ_`abdfghijklmnopqrstuvwxyz{|}~')
BW_LETTERS_CHARSET = frozenset(u'$&\'*<>ADEGHJPSTVYZ_bdfghjklmnpqrstvwxyz{|}')
BW_DIAC_CHARSET = frozenset(u'FKN`aiou~')

SAFEBW_CHARSET = frozenset(
    u'ABCDEFGHIJKLMNOPQSTVWYZ_abcdefghijklmnopqrstuvwxyz~')
SAFEBW_LETTERS_CHARSET = frozenset(
    u'ABCDEGHIJLMOPQSTVWYZ_bcdefghjklmnpqrstvwxyz')
SAFEBW_DIAC_CHARSET = frozenset(u'FKNaeiou~')

XMLBW_CHARSET = frozenset(
    u'$\'*ABDEFGHIJKNOPSTWYZ_`abdfghijklmnopqrstuvwxyz{|}~')
XMLBW_LETTERS_CHARSET = frozenset(
    u'$\'*ABDEGHIJOPSTWYZ_bdfghjklmnpqrstvwxyz{|}')
XMLBW_DIAC_CHARSET = frozenset(u'FKN`aiou~')

HSB_CHARSET = frozenset(u'\'.ADHST_abcdfghijklmnpqrstuvwxyz~'
                        u'ÂÄáãðýĀĂĎħĩšũŵŷγθς')
HSB_LETTERS_CHARSET = frozenset(u'\'ADHST_bcdfghjklmnpqrstvwxyz'
                                u'ÂÄáðýĀĂĎħšŵŷγθς')
HSB_DIAC_CHARSET = frozenset(u'.aiu~Äáãĩũ')
