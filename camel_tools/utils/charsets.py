# -*- coding: utf-8 -*-

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
