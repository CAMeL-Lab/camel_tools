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

"""The reinflector component of CALIMA Star.
"""

from __future__ import absolute_import

from collections import deque

import re

from camel_tools.calima_star.database import CalimaStarDB
from camel_tools.calima_star.analyzer import CalimaStarAnalyzer
from camel_tools.calima_star.generator import CalimaStarGenerator
from camel_tools.calima_star.errors import ReinflectorError
from camel_tools.calima_star.errors import InvalidReinflectorFeature
from camel_tools.calima_star.errors import InvalidReinflectorFeatureValue
from camel_tools.utils.dediac import dediac_ar


_CLITIC_FEATS = frozenset(['enc0', 'prc0', 'prc1', 'prc2', 'prc3'])
_IGNORED_FEATS = frozenset(['diac', 'lex', 'bw', 'gloss', 'source', 'stem',
                            'stemcat', 'lmm', 'dediac', 'caphi', 'catib6',
                            'ud', 'd3seg', 'atbseg', 'd2seg', 'd1seg', 'd1tok',
                            'd2tok', 'atbtok', 'd3tok', 'root', 'pattern',
                            'freq', 'pos_freq', 'lex_freq', 'pos_lex_freq',
                            'stemgloss'])
_SPECIFIED_FEATS = frozenset(['form_gen', 'form_num'])
_CLITIC_IGNORED_FEATS = frozenset(['stt', 'cas', 'mod'])
_FILTER_FEATS = frozenset(['pos', 'lex'])

_LEMMA_SPLIT_RE = re.compile(u'-|_')


class CalimaStarReinflector(object):
    """CALIMA Star reinflector component.

    Arguments:
        db (:obj:`~camel_tools.calima_star.database.CalimaStarDB`): Database to
            use for generation. Must be opened in reinflection mode or both
            analysis and generation modes.

    Raises:
        :obj:`~camel_tools.calima_star.errors.ReinflectorError`: If **db** is
            not an instance of
            :obj:`~camel_tools.calima_star.database.CalimaStarDB` or if **db**
            does not support reinflection.
    """

    def __init__(self, db):
        if not isinstance(db, CalimaStarDB):
            raise ReinflectorError('DB is not an instance of CalimaStarDB')
        if not db.flags.generation:
            raise ReinflectorError('DB does not support reinflection')

        self._db = db

        self._analyzer = CalimaStarAnalyzer(db)
        self._generator = CalimaStarGenerator(db)

    def reinflect(self, word, feats):
        """Generate analyses for a given word from a given set of inflectional
        features.

        Arguments:
            word (:obj:`str`): Word to reinflect.
            feats (:obj:`dict`): Dictionary of features.
                See :doc:`/reference/calima_star_features` for more information
                on features and their values.

        Returns:
            :obj:`list` of :obj:`dict`: List of generated analyses.
            See :doc:`/reference/calima_star_features` for more information on
            features and their values.

        Raises:
            :obj:`~camel_tools.calima_star.errors.InvalidReinflectorFeature`:
                If a feature is given that is not defined in database.
            :obj:`~camel_tools.calima_star.errors.InvalidReinflectorFeatureValue`:
                If an invalid value is given to a feature or if 'pos' feature
                is not defined.
        """

        analyses = self._analyzer.analyze(word)

        if not analyses or len(analyses) == 0:
            return []

        for feat in feats:
            if feat not in self._db.defines:
                raise InvalidReinflectorFeature(feat)
            elif (self._db.defines[feat] is not None and
                  feats[feat] not in self._db.defines[feat]):
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
                        if analysis[feat] != 'na':
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

        return list(results)
