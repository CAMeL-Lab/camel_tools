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


"""This module provides functions for normalizing Arabic text.
"""


import re
import unicodedata


_ALEF_NORMALIZE_BW_RE = re.compile(u'[<>{|]')
_ALEF_NORMALIZE_SAFEBW_RE = re.compile(u'[IOLM]')
_ALEF_NORMALIZE_XMLBW_RE = re.compile(u'[IO{|]')
_ALEF_NORMALIZE_HSB_RE = re.compile(u'[\u0102\u00c2\u00c4\u0100]')
_ALEF_NORMALIZE_AR_RE = re.compile(u'[\u0625\u0623\u0671\u0622]')


def normalize_unicode(s, compatibility=True):
    """Normalize Unicode strings into their canonically composed form or
    (i.e. characters that can be written as a combination of unicode characters
    are converted to their single character form).

    Note: This is essentially a call to :func:`unicodedata.normalize` with
    form 'NFC' if **compatibility** is False or 'NFKC' if it's True.

    Args:
        s (:obj:`str`): The string to be normalized.
        compatibility (:obj:`bool`, optional): Apply compatibility
            decomposition. Defaults to True.

    Returns:
        :obj:`str`: The normalized string.
    """

    if compatibility:
        return unicodedata.normalize('NFKC', s)
    return unicodedata.normalize('NFC', s)


def normalize_alef_maksura_bw(s):
    """Normalize all occurences of Alef Maksura characters to a Yeh character
    in a Buckwalter encoded string.

    Args:
        s (:obj:`str`): The string to be normalized.

    Returns:
        :obj:`str`: The normalized string.
    """

    return s.replace(u'Y', u'y')


def normalize_alef_maksura_safebw(s):
    """Normalize all occurences of Alef Maksura characters to a Yeh character
    in a Safe Buckwalter encoded string.

    Args:
        s (:obj:`str`): The string to be normalized.

    Returns:
        :obj:`str`: The normalized string.
    """

    return s.replace(u'Y', u'y')


def normalize_alef_maksura_xmlbw(s):
    """Normalize all occurences of Alef Maksura characters to a Yeh character
    in a XML Buckwalter encoded string.

    Args:
        s (:obj:`str`): The string to be normalized.

    Returns:
        :obj:`str`: The normalized string.
    """

    return s.replace(u'Y', u'y')


def normalize_alef_maksura_hsb(s):
    """Normalize all occurences of Alef Maksura characters to a Yeh character
    in a Habash-Soudi-Buckwalter encoded string.

    Args:
        s (:obj:`str`): The string to be normalized.

    Returns:
        :obj:`str`: The normalized string.
    """

    return s.replace(u'\u00fd', u'y')


def normalize_alef_maksura_ar(s):
    """Normalize all occurences of Alef Maksura characters to a Yeh character
    in an Arabic string.

    Args:
        s (:obj:`str`): The string to be normalized.

    Returns:
        :obj:`str`: The normalized string.
    """

    return s.replace(u'\u0649', u'\u064a')


def normalize_teh_marbuta_bw(s):
    """Normalize all occurences of Teh Marbuta characters to a Heh character
    in a Buckwalter encoded string.

    Args:
        s (:obj:`str`): The string to be normalized.

    Returns:
        :obj:`str`: The normalized string.
    """

    return s.replace(u'p', u'h')


def normalize_teh_marbuta_safebw(s):
    """Normalize all occurences of Teh Marbuta characters to a Heh character
    in a Safe Buckwalter encoded string.

    Args:
        s (:obj:`str`): The string to be normalized.

    Returns:
        :obj:`str`: The normalized string.
    """

    return s.replace(u'p', u'h')


def normalize_teh_marbuta_xmlbw(s):
    """Normalize all occurences of Teh Marbuta characters to a Heh character
    in a XML Buckwalter encoded string.

    Args:
        s (:obj:`str`): The string to be normalized.

    Returns:
        :obj:`str`: The normalized string.
    """

    return s.replace(u'p', u'h')


def normalize_teh_marbuta_hsb(s):
    """Normalize all occurences of Teh Marbuta characters to a Heh character
    in a Habash-Soudi-Buckwalter encoded string.

    Args:
        s (:obj:`str`): The string to be normalized.

    Returns:
        :obj:`str`: The normalized string.
    """

    return s.replace(u'\u0127', u'h')


def normalize_teh_marbuta_ar(s):
    """Normalize all occurences of Teh Marbuta characters to a Heh character
    in an Arabic string.

    Args:
        s (:obj:`str`): The string to be normalized.

    Returns:
        :obj:`str`: The normalized string.
    """

    return s.replace(u'\u0629', u'\u0647')


def normalize_alef_bw(s):
    """Normalize various Alef variations to plain a Alef character in a
    Buckwalter encoded string.

    Args:
        s (:obj:`str`): The string to be normalized.

    Returns:
        :obj:`str`: The normalized string.
    """

    return _ALEF_NORMALIZE_BW_RE.sub(u'A', s)


def normalize_alef_safebw(s):
    """Normalize various Alef variations to plain a Alef character in a
    Safe Buckwalter encoded string.

    Args:
        s (:obj:`str`): The string to be normalized.

    Returns:
        :obj:`str`: The normalized string.
    """

    return _ALEF_NORMALIZE_SAFEBW_RE.sub(u'A', s)


def normalize_alef_xmlbw(s):
    """Normalize various Alef variations to plain a Alef character in a
    XML Buckwalter encoded string.

    Args:
        s (:obj:`str`): The string to be normalized.

    Returns:
        :obj:`str`: The normalized string.
    """

    return _ALEF_NORMALIZE_XMLBW_RE.sub(u'A', s)


def normalize_alef_hsb(s):
    """Normalize various Alef variations to plain a Alef character in a
    Habash-Soudi-Buckwalter encoded string.

    Args:
        s (:obj:`str`): The string to be normalized.

    Returns:
        :obj:`str`: The normalized string.
    """

    return _ALEF_NORMALIZE_HSB_RE.sub(u'A', s)


def normalize_alef_ar(s):
    """Normalize various Alef variations to plain a Alef character in an
    Arabic string.

    Args:
        s (:obj:`str`): The string to be normalized.

    Returns:
        :obj:`str`: The normalized string.
    """

    return _ALEF_NORMALIZE_AR_RE.sub(u'\u0627', s)
