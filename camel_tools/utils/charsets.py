# -*- coding: utf-8 -*-

"""Contains character sets for different encoding schemes as well as Unicode
characters marked as symbols and punctuation.
"""

import unicodedata


UNICODE_PUNCT_CHARSET = frozenset(
    [chr(x) for x in range(65536) if unicodedata.category(chr(x))[0] == 'P'])
UNICODE_SYMBOL_CHARSET = frozenset(
    [chr(x) for x in range(65536) if unicodedata.category(chr(x))[0] == 'S'])

AR_CHARSET = frozenset(u'ءآأؤإئابةتثجحخدذرزسشصضطظعغـفقكلمنهوىيًٌٍَُِّْٰٱپڤگءآأؤإئابةتثجحخدذرزسشصضطظعغـفقكلمنهوىيًٌٍَُِّْٰٱپچڤگ')
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

HSB_CHARSET = frozenset(u'\'.ADHST_abcdfghijklmnpqrstuvwxyz~ÂÄáãðýĀĂĎħĩšũŵŷγθς')
HSB_LETTERS_CHARSET = frozenset(u'\'ADHST_bcdfghjklmnpqrstvwxyzÂÄáðýĀĂĎħšŵŷγθς')
HSB_DIAC_CHARSET = frozenset(u'.aiu~Äáãĩũ')
