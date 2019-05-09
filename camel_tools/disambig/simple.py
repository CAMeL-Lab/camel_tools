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


"""Contains a simple disambiguator class that ranks analyses based on their
POS-Lex frequency.
"""


from collections import deque

from camel_tools.disambig.common import ScoredAnalysis, DisambiguatedWord
from camel_tools.disambig.common import Disambiguator


def _get_pos_lex_freq(analysis):
    freq = analysis.get('pos_lex_freq', -99.0)
    if freq is None:
        return -99
    return freq


class SimpleDisambiguator(Disambiguator):
    '''A simple disambiguator function that ranks analyses based on their
    pos-lex frequencies.

    Args:
        analyzer (:obj:`~camel_tools.calima_star.analazer.CalimaStarAnalyzer`):
            Morphological analyzer used to generate the pos-lex frequencies.
    '''

    def __init__(self, analyzer):
        self._analyzer = analyzer

    def disambiguate(self, sentence, top=1):
        analyzed_words = self._analyzer.analyze_words(sentence)
        result = deque()

        for word, analyses in analyzed_words:
            if len(analyses) == 0:
                result.append(DisambiguatedWord(word, []))
                continue

            probabilities = [10 ** _get_pos_lex_freq(a) for a in analyses]
            max_prob = max(probabilities)

            scored_analyses = [ScoredAnalysis(p / max_prob, a)
                               for a, p in zip(analyses, probabilities)]

            scored_analyses.sort(key=lambda w: w.score, reverse=True)

            if top < 1:
                result.append(DisambiguatedWord(word, scored_analyses))
            else:
                result.append(DisambiguatedWord(word, scored_analyses[0:top]))

        return list(result)
