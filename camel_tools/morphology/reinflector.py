# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2025 New York University Abu Dhabi
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

"""The reinflector component of CAMeL Tools.
"""

from __future__ import absolute_import

from collections import deque

import re

from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.morphology.generator import Generator
from camel_tools.morphology.errors import ReinflectorError
from camel_tools.morphology.errors import InvalidReinflectorFeature
from camel_tools.morphology.errors import InvalidReinflectorFeatureValue
from camel_tools.utils.dediac import dediac_ar


_CLITIC_FEATS = frozenset(['enc0', 'prc0', 'prc1', 'prc2', 'prc3'])
_IGNORED_FEATS = frozenset(['diac', 'lex', 'bw', 'gloss', 'source', 'stem',
                            'stemcat', 'lmm', 'dediac', 'caphi', 'catib6',
                            'ud', 'd3seg', 'atbseg', 'd2seg', 'd1seg', 'd1tok',
                            'd2tok', 'atbtok', 'd3tok', 'bwtok', 'root',
                            'pattern', 'freq', 'pos_logprob', 'lex_logprob',
                            'pos_lex_logprob', 'stemgloss'])
_SPECIFIED_FEATS = frozenset(['form_gen', 'form_num'])
_CLITIC_IGNORED_FEATS = frozenset(['stt', 'cas', 'mod'])
_FILTER_FEATS = frozenset(['pos', 'lex'])
_ANY_FEATS = frozenset(['per', 'gen', 'num', 'cas', 'stt', 'vox', 'mod',
                        'asp'])

_LEMMA_SPLIT_RE = re.compile(u'-|_')


class Reinflector(object):
    """Morphological reinflector component.

    Arguments:
        db (:obj:`~camel_tools.morphology.database.MorphologyDB`): Database to
            use for generation. Must be opened in reinflection mode or both
            analysis and generation modes.

    Raises:
        :obj:`~camel_tools.morphology.errors.ReinflectorError`: If **db** is
            not an instance of
            :obj:`~camel_tools.morphology.database.MorphologyDB` or if **db**
            does not support reinflection.
    """

    def __init__(self, db):
        if not isinstance(db, MorphologyDB):
            raise ReinflectorError('DB is not an instance of MorphologyDB')
        if not db.flags.generation:
            raise ReinflectorError('DB does not support reinflection')

        self._db = db

        self._analyzer = Analyzer(db)
        self._generator = Generator(db)

    def reinflect(self, word, feats):
        """Generate surface forms and their associated analyses for a given 
        word and a given set of (possibly underspecified) features. 
        The surface form is accessed through the `diac` feature.

        Arguments:
            word (:obj:`str`): Word to reinflect.
            feats (:obj:`dict`): Dictionary of features.
                See :doc:`/reference/camel_morphology_features` for more
                information on features and their values.

        Returns:
            :obj:`list` of :obj:`dict`: List of generated analyses.
            See :doc:`/reference/camel_morphology_features` for more
            information on features and their values.

        Raises:
            :obj:`~camel_tools.morphology.errors.InvalidReinflectorFeature`:
                If a feature is given that is not defined in database.
            :obj:`~camel_tools.morphology.errors.InvalidReinflectorFeatureValue`:
                If an invalid value is given to a feature or if 'pos' feature
                is not defined.
        """

        analyses = self._analyzer.analyze(word)

        if not analyses or len(analyses) == 0:
            return []

        for feat in feats:
            if feat not in self._db.defines:
                raise InvalidReinflectorFeature(feat)
            elif self._db.defines[feat] is not None:
                if feat in _ANY_FEATS and feats[feat] == 'ANY':
                    continue
                elif feats[feat] not in self._db.defines[feat]:
                    raise InvalidReinflectorFeatureValue(feat, feats[feat])

        has_clitics = False
        for feat in _CLITIC_FEATS:
            if feat in feats:
                has_clitics = True
                break

        results = deque()

        for analysis in analyses:
            if dediac_ar(analysis['diac']) != dediac_ar(word):
                continue

            if 'pos' in feats and feats['pos'] != analysis['pos']:
                continue

            lemma = _LEMMA_SPLIT_RE.split(analysis['lex'])[0]

            if 'lex' in feats and feats['lex'] != lemma:
                continue

            is_valid = True
            generate_feats = {}

            for feat in analysis.keys():
                if feat in _IGNORED_FEATS:
                    continue
                elif feat in _SPECIFIED_FEATS and feat not in feats:
                    continue
                elif has_clitics and feat in _CLITIC_IGNORED_FEATS:
                    continue
                else:
                    if feat in feats:
                        if feats[feat] == 'ANY':
                            continue
                        elif analysis[feat] != 'na':
                            generate_feats[feat] = feats[feat]
                        else:
                            is_valid = False
                            break
                    elif analysis[feat] != 'na':
                        generate_feats[feat] = analysis[feat]

            if is_valid:
                generated = self._generator.generate(lemma, generate_feats)
                if generated is not None:
                    results.extend(generated)
        
        # TODO: Temporary fix to get unique analyses
        results  = [dict(y) for y in set(tuple(x.items()) for x in results)]

        return list(results)

    def all_feats(self):
        """Return a set of all features provided by the database used in this
        reinflector instance.

        Returns:
            :obj:`frozenset` of :obj:`str`: The set all features provided by
            the database used in this reinflector instance.
        """

        return self._db.all_feats()

    def tok_feats(self):
        """Return a set of tokenization features provided by the database used
        in this reinflector instance.

        Returns:
            :obj:`frozenset` of :obj:`str`: The set tokenization features
            provided by the database used in this reinflector instance.
        """
        return self._db.tok_feats()
