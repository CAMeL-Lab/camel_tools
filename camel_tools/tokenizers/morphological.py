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


"""This module contains utilities for morphological tokenization.
"""


import re
from collections import deque
from camel_tools.utils.dediac import dediac_ar


# Reduce consequitive '+'s to one
_REMOVE_PLUSES = re.compile(r'(_\+|\+_)+')

def _default_dediac(tok):
    return dediac_ar(tok)


def _bwtok_dediac(tok):
    return _REMOVE_PLUSES.sub(r'\g<1>', dediac_ar(tok).strip('+_'))

_DIAC_TYPE = {
    'atbtok': _default_dediac,
    'atbseg': _default_dediac,
    'bwtok': _bwtok_dediac,
    'd1tok': _default_dediac,
    'd1seg': _default_dediac,
    'd2tok': _default_dediac,
    'd2seg': _default_dediac,
    'd3tok': _default_dediac,
    'd3seg': _default_dediac
}


class MorphologicalTokenizer(object):
    """Class for morphologically tokenizing Arabic words.

    Args:
        disambiguator (:obj:`~camel_tools.disambig.common.Disambiguator`): The
            disambiguator to use for tokenization.
        scheme (:obj:`str`): The tokenization scheme to use.
            You can use the
            :meth:`~camel_tools.disambig.common.Disambiguator.tok_feats`
            method of your chosen disambiguator to get a list of tokenization
            schemes it produces.
        split (:obj:`bool`, optional): If set to True, then morphological
            tokens will be split into separate strings, otherwise they will be
            delimited by an underscore. Defaults to False.
        diac (:obj:`bool`, optional): If set to True, then output tokens will
            be diacritized, otherwise they will be undiacritized.
            Defaults to False.
            Note that when the tokenization scheme is set to 'bwtok', the
            number of produced undiacritized tokens might be less than the
            diacritized tokens becuase the 'bwtok' scheme can have
            morphemes that are standalone diacritics (e.g. case and mood).
    """

    def __init__(self, disambiguator, scheme, split=False,
                 diac=False):
        self._disambiguator = disambiguator
        self._scheme = scheme
        self._split = split
        self._diacf = lambda w: w if diac else _DIAC_TYPE[self._scheme](w)

    def tokenize(self, words):
        """Generate morphological tokens for a given list of words.

        Args:
            words (:obj:`list` of :obj:`str`): List of words to tokenize.

        Returns:
            :obj:`list` of :obj:`str`: List of morphologically tokenized words.
        """

        disambig_words = self._disambiguator.disambiguate(words)
        result = deque()

        for disambig_word in disambig_words:
            scored_analyses = disambig_word.analyses
            if len(scored_analyses) > 0:
                analysis = scored_analyses[0].analysis
                tok = analysis.get(self._scheme, None)

                if tok is None or tok == 'NOAN':
                    tok = disambig_word.word
                    result.append(self._diacf(tok))
                elif self._split:
                    tok = self._diacf(tok)
                    result.extend(tok.split('_'))
                else:
                    result.append(self._diacf(tok))

            else:
                result.append(disambig_word.word)

        return list(result)
