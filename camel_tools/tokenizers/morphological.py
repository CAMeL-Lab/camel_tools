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


"""This module contains utilities for morphological tokenization.
"""


from collections import deque


_SCHEME_SET = frozenset(['atbtok', 'd3tok'])


class MorphologicalTokenizer(object):
    """Class for morphologically tokenizing Arabic words.

    Args:
        disambiguator (:obj:`~camel_tools.disambig.common.Disambiguator`): The
            disambiguator to use for tokenization.
        scheme (:obj:`str`, optional): The tokenization scheme to use.
            Defaults to 'atbtok'. See :doc:`/reference/calima_star_features`
            for more information on available tokenization schemes.
        split (:obj:`bool`, optional): If set to True, then morphological
            tokens will be split into separate strings, otherwise they will be
            delimited by an underscore. Defaults to False.
    """

    def __init__(self, disambiguator, scheme='atbtok', split=False):
        self._disambiguator = disambiguator
        self._scheme = scheme
        self._split = split

    @classmethod
    def scheme_set(cls):
        """Returns a set of supported tokenization schemes.

        Returns:
            :obj:`frozenset` of :obj:`str`: set of supported tokenization
            schemes.
        """
        return _SCHEME_SET

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

                if tok is None:
                    tok = disambig_word.word
                    result.append(tok)
                elif self._split:
                    result.extend(tok.split('_'))
                else:
                    result.append(tok)

            else:
                result.append(disambig_word.word)

        return list(result)
