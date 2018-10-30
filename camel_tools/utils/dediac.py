# -*- coding: utf-8 -*-
"""This submodule contains functions for dediacritizing Arabic text in
different encodings.
"""

from __future__ import absolute_import

import regex as re

from camel_tools.utils.charsets import AR_DIAC_CHARSET, BW_DIAC_CHARSET
from camel_tools.utils.charsets import SAFEBW_DIAC_CHARSET, XMLBW_DIAC_CHARSET
from camel_tools.utils.charsets import HSB_DIAC_CHARSET


_DIAC_RE_BW = re.compile(r'[' + re.escape(''.join(BW_DIAC_CHARSET)) + ']')
_DIAC_RE_SAFEBW = re.compile(r'[' + re.escape(''.join(SAFEBW_DIAC_CHARSET)) +
                             ']')
_DIAC_RE_XMLBW = re.compile(r'[' + re.escape(''.join(XMLBW_DIAC_CHARSET)) +
                            ']')
_DIAC_RE_HSB = re.compile(r'[' + re.escape(''.join(HSB_DIAC_CHARSET)) + ']')
_DIAC_RE_AR = re.compile(r'[' + re.escape(''.join(AR_DIAC_CHARSET)) + ']')


def dediac_bw(s):
    return _DIAC_RE_BW.sub('', s)


def dediac_safebw(s):
    return _DIAC_RE_SAFEBW.sub('', s)


def dediac_xmlbw(s):
    return _DIAC_RE_XMLBW.sub('', s)


def dediac_hsb(s):
    return _DIAC_RE_HSB.sub('', s)


def dediac_ar(s):
    return _DIAC_RE_AR.sub('', s)
