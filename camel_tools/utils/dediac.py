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

"""This submodule contains functions for dediacritizing Arabic text in
different encodings. See :doc:`/reference/encoding_schemes` for more
information on encodings.
"""

from __future__ import absolute_import

import re

from camel_tools.utils.charsets import AR_DIAC_CHARSET, BW_DIAC_CHARSET
from camel_tools.utils.charsets import SAFEBW_DIAC_CHARSET, XMLBW_DIAC_CHARSET
from camel_tools.utils.charsets import HSB_DIAC_CHARSET


_DIAC_RE_BW = re.compile(u'[' +
                         re.escape(u''.join(BW_DIAC_CHARSET)) +
                         u']')
_DIAC_RE_SAFEBW = re.compile(u'[' +
                             re.escape(u''.join(SAFEBW_DIAC_CHARSET)) +
                             u']')
_DIAC_RE_XMLBW = re.compile(u'[' +
                            re.escape(u''.join(XMLBW_DIAC_CHARSET)) +
                            u']')
_DIAC_RE_HSB = re.compile(u'[' +
                          re.escape(u''.join(HSB_DIAC_CHARSET)) +
                          u']')
_DIAC_RE_AR = re.compile(u'[' +
                         re.escape(u''.join(AR_DIAC_CHARSET)) +
                         u']')


def dediac_bw(s):
    """Dediacritize Buckwalter encoded string.

    Args:
        s (:obj:`str`): String to dediacritize.

    Returns:
        :obj:`str`: Dediacritized string.
    """

    return _DIAC_RE_BW.sub(u'', s)


def dediac_safebw(s):
    """Dediacritize Safe Buckwalter encoded string.

    Args:
        s (:obj:`str`): String to dediacritize.

    Returns:
        :obj:`str`: Dediacritized string.
    """

    return _DIAC_RE_SAFEBW.sub(u'', s)


def dediac_xmlbw(s):
    """Dediacritize XML Buckwalter encoded string.

    Args:
        s (:obj:`str`): String to dediacritize.

    Returns:
        :obj:`str`: Dediacritized string.
    """

    return _DIAC_RE_XMLBW.sub(u'', s)


def dediac_hsb(s):
    """Dediacritize Habash-Soudi-Buckwalter encoded string.

    Args:
        s (:obj:`str`): String to dediacritize.

    Returns:
        :obj:`str`: Dediacritized string.
    """

    return _DIAC_RE_HSB.sub(u'', s)


def dediac_ar(s):
    """Dediacritize Unicode Arabic string.

    Args:
        s (:obj:`str`): String to dediacritize.

    Returns:
        :obj:`str`: Dediacritized string.
    """

    return _DIAC_RE_AR.sub(u'', s)
