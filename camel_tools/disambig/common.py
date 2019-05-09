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


"""This sub-module contains common functions and classes used for
disambiguation.
"""


from abc import ABC, abstractmethod
from collections import namedtuple


class ScoredAnalysis(namedtuple('ScoredAnalysis', ['score', 'analysis'])):
    """A named tuple containing an analysis and its score.

    Attributes:
        score (:obj:`float`): The score of a given analysis.

        analysis (:obj:`dict`): The analysis dictionary.
            See :doc:`/reference/calima_star_features` for more information on
            features and their values.
    """


class DisambiguatedWord(namedtuple('DisambiguatedWord', ['word', 'analyses'])):
    """A named tuple containing a word and a sorted list (from high to low
    score) of scored analyses.

    Attributes:
        word (:obj:`str`): The word being disambiguated.

        analyses (:obj:`list` of \
        :obj:`~camel_tools.disambig.common.ScoredAnalysis`): List of scored
            analyses sorted from highest to lowest disambiguation score.
    """


class Disambiguator(ABC):
    """Abstract base class that all disambiguators should implement.
    """

    @abstractmethod
    def disambiguate(self, sentence, top=1):
        """Disambiguate words in a sentence.

        Args:
            sentence (:obj:`list` of :obj:`str`): list of words representing a
                sentence to be disambiguated.
            top (:obj:`int`, optional): The number of top analyses to return.
                If set to zero or less, then all analyses are returned.
                Defaults to 1.

        Returns:
        :obj:`list` of :obj:`~camel_tools.disambig.common.DisambiguatedWord`:
        List of disambiguted words in **sentence**.
        """

        return NotImplemented

    @abstractmethod
    def disambiguate_word(self, sentence, word_ndx, top=1):
        """Disambiguate a word at a given index in a sentence.

        Args:
            sentence (:obj:`list` of :obj:`str`): list of words representing a
                sentence.
            word_ndx (:obj:`int`): the index of the word in **sentence** to
                disambiguate.
            top (:obj:`int`, optional): The number of top analyses to return.
                If set to zero or less, then all analyses are returned.
                Defaults to 1.

        Returns:
        :obj:`~camel_tools.disambig.common.DisambiguatedWord`: The
        disambiguated word at index **word_ndx** in **sentence**.
        """

        return NotImplemented
