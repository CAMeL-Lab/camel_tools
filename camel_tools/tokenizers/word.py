# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2026 New York University Abu Dhabi
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


"""This module contains utilities for word-boundary tokenization."""


import regex as re

from camel_tools.utils.charsets import EMOJI_ALL_CHARSET, UNICODE_PUNCT_SYMBOL_CHARSET


__all__ = ["simple_word_tokenize"]


_SYMBOLS_ALL = frozenset() | UNICODE_PUNCT_SYMBOL_CHARSET | EMOJI_ALL_CHARSET

# Matches possible Emoji sequences, symbols and punctuation.
# Based on the regex suggested in UTS #51: https://www.unicode.org/reports/tr51/#EBNF_and_Regex
_SYMBOLS_RE = re.compile(
    # TODO: Refactor this using verbose mode.
    r"(?:(?:\p{RI}\p{RI}|\p{Emoji}(?:\p{EMod}|\uFE0F\u20E3?|[\U000E0020-\U000E007E]+\U000E007F)?(?:\u200D(?:\p{RI}\p{RI}|\p{Emoji}(?:\p{EMod}|\uFE0F\u20E3?|[\U000E0020-\U000E007E]+\U000E007F)?))*)|(?:[0-9*#]\u20e3)|\p{S}|\p{P})"
)

_DIGITS_RE = re.compile(r"\d+")


def _simple_word_tokenize(s: str):
    tokens = []

    for word in s.split():
        word_len = len(word)
        curr_ndx = 0
        curr_start = 0

        while curr_ndx < word_len:
            # Check if the current start is an emoji or symbol
            symbol_match = _SYMBOLS_RE.match(word, pos=curr_ndx)
            if symbol_match is not None:
                match_str = symbol_match[0]
                if match_str in _SYMBOLS_ALL:
                    if curr_ndx != curr_start:
                        tokens.append(word[curr_start:curr_ndx])
                    tokens.append(match_str)
                    curr_ndx = curr_start = symbol_match.end()
                    continue

            curr_ndx += 1

        last = word[curr_start:curr_ndx]
        if len(last):
            tokens.append(word[curr_start:])

    return tokens


def _simple_word_tokenize_split_digit(s: str):
    tokens = []

    for word in s.split():
        word_len = len(word)
        curr_ndx = 0
        curr_start = 0

        while curr_ndx < word_len:
            # Check if the current start is an emoji or symbol
            symbol_match = _SYMBOLS_RE.match(word, pos=curr_ndx)
            if symbol_match is not None:
                match_str = symbol_match[0]
                if match_str in _SYMBOLS_ALL:
                    if curr_ndx != curr_start:
                        tokens.append(word[curr_start:curr_ndx])
                    tokens.append(match_str)
                    curr_ndx = curr_start = symbol_match.end()
                    continue

            # Check if we are at a digit sequence
            digit_match = _DIGITS_RE.match(word, pos=curr_ndx)
            if digit_match is not None:
                if curr_ndx != curr_start:
                    tokens.append(word[curr_start:curr_ndx])
                tokens.append(digit_match[0])
                curr_ndx = curr_start = digit_match.end()
                continue

            curr_ndx += 1

        last = word[curr_start:curr_ndx]
        if len(last):
            tokens.append(word[curr_start:])

    return tokens


def simple_word_tokenize(s, split_digits = False):
    """Tokenizes a sentence by splitting on whitespace and separating
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
        return _simple_word_tokenize_split_digit(s)

    return _simple_word_tokenize(s)
