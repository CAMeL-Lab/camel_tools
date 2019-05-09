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


"""This module contains utilities for word-boundary tokenization.
"""


import re

from camel_tools.utils.charsets import UNICODE_PUNCT_SYMBOL_CHARSET


_ALL_PUNCT = u''.join(UNICODE_PUNCT_SYMBOL_CHARSET)
_TOKENIZE_RE = re.compile(r'[' + re.escape(_ALL_PUNCT) + r']|\w+')


def simple_word_tokenize(sentence):
    """Tokenizes a sentence by splitting on whitespace and seperating
    punctuation. The resulting tokens are either alpha-numeric words or single
    punctuation/symbol characters.
    For example, tokenizing :code:`'Hello, world!!!'`
    would yield :code:`['Hello', ',', 'world', '!', '!', '!']`.

    Args:
        sentence (:obj:`str`): Sentence to tokenize.

    Returns:
        :obj:`list` of :obj:`str`: The list of tokens.
    """

    return _TOKENIZE_RE.findall(sentence)
