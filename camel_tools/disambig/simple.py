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


"""Contains a simple disambiguator function that ranks analyses based on their
POS-Lex frequency.
"""


from collections import deque


def _POS_LEX_SORT_KEY(analysis):
    return analysis.get('pos_lex_freq', -99.0)


def simple_disambig(analyses, top=1):
    '''A simple disambiguation function that ranks analyses based on their
    pos-lex frequencies.

    Args:
        analyses (:obj:`list` of :obj:`tuple` of \
        (:obj:`str`, :obj:`list` of :obj:`dict`)): List of word-analyses pairs.
        top (:obj:`int`, optional): The number of top analyses to return.
            Defaults to 1.

    Returns:
        :obj:`list` of :obj:`tuple` of (:obj:`str`, :obj:`dict`):
        List of word-analyses pairs with the top most frquent analyses.
    '''

    if analyses is None:
        return None

    top = max(1, int(top))
    result = deque()

    for word, analysis in analyses:
        sorted_analyses = sorted(analysis, key=_POS_LEX_SORT_KEY, reverse=True)
        result.append((word, sorted_analyses[0:top]))

    return list(result)
