# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2022 New York University Abu Dhabi
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


"""This module contains utilities for word-boundary tokenization.
"""


import re

from camel_tools.utils.charsets import UNICODE_PUNCT_SYMBOL_CHARSET
from camel_tools.utils.charsets import UNICODE_LETTER_MARK_NUMBER_CHARSET
from camel_tools.utils.charsets import UNICODE_LETTER_CHARSET
from camel_tools.utils.charsets import UNICODE_MARK_CHARSET
from camel_tools.utils.charsets import UNICODE_NUMBER_CHARSET
from camel_tools.utils.charsets import EMOJI_MULTICHAR_CHARSET


__all__ = ['simple_word_tokenize']


_ALL_PUNCT_SYMBOLS = (UNICODE_PUNCT_SYMBOL_CHARSET | EMOJI_MULTICHAR_CHARSET)
_ALL_PUNCT_SYMBOLS = [re.escape(x) for x in _ALL_PUNCT_SYMBOLS]
_ALL_PUNCT_SYMBOLS = sorted(_ALL_PUNCT_SYMBOLS, key=len, reverse=True)

_ALL_NUMBER = u''.join(UNICODE_NUMBER_CHARSET)
_ALL_LETTER_MARK = u''.join((UNICODE_LETTER_CHARSET | UNICODE_MARK_CHARSET))
_ALL_LETTER_MARK_NUMBER = u''.join(UNICODE_LETTER_MARK_NUMBER_CHARSET)

_TOKENIZE_RE = re.compile(u'|'.join(_ALL_PUNCT_SYMBOLS) + r'|[' +
                          re.escape(_ALL_LETTER_MARK_NUMBER) + r']+')
_TOKENIZE_NUMBER_RE = re.compile(u'|'.join(_ALL_PUNCT_SYMBOLS) + r'|[' +
                                 re.escape(_ALL_NUMBER) + r']+|[' +
                                 re.escape(_ALL_LETTER_MARK) + r']+')


def simple_word_tokenize(sentence, split_digits=False):
    """Tokenizes a sentence by splitting on whitespace and seperating
    punctuation. The resulting tokens are either alpha-numeric words, single
    punctuation/symbol/emoji characters, or multi-character emoji sequences.
    This function is language agnostic and splits all characters marked as
    punctuation or symbols in the Unicode specification.
    For example, tokenizing :code:`'Hello,    world!!!'`
    would yield :code:`['Hello', ',', 'world', '!', '!', '!']`.
    If split_digits is set to True, it also splits on number.
    For example, tokenizing :code:`'Hello,    world123!!!'`
    would yield :code:`['Hello', ',', 'world', '123', '!', '!', '!']`.

    Args:
        sentence (:obj:`str`): Sentence to tokenize.
        split_digits (:obj:`bool`, optional): The flag to split on number.
            Defaults to False.

    Returns:
        :obj:`list` of :obj:`str`: The list of tokens.
    """

    if split_digits:
        return _TOKENIZE_NUMBER_RE.findall(sentence)
    else:
        return _TOKENIZE_RE.findall(sentence)
