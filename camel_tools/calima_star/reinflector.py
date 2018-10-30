# -*- coding: utf-8 -*-

"""The generator component of CALIMA Star.
"""

from __future__ import absolute_import

from collections import deque

import re

from camel_tools.calima_star.analyzer import CalimaStarAnalyzer
from camel_tools.calima_star.generator import CalimaStarGenerator
from camel_tools.utils.dediac import dediac_ar


_CLITIC_FEATS = frozenset(['enc0', 'prc0', 'prc1', 'prc2', 'prc3'])
_IGNORED_FEATS = frozenset(['diac', 'lex', 'bw', 'gloss', 'source', 'stem',
                            'stemcat', 'lmm', 'dediac', 'caphi', 'catib6',
                            'ud', 'd3seg', 'atbseg', 'd2seg', 'd1seg', 'd1tok',
                            'd2tok', 'atbtok', 'd3tok', 'root', 'pattern',
                            'freq', 'POS_prob', 'stemgloss'])
_SPECIFIED_FEATS = frozenset(['form_gen', 'form_num'])
_CLITIC_IGNORED_FEATS = frozenset(['stt', 'cas', 'mod'])
_FILTER_FEATS = frozenset(['pos', 'lex'])

_LEMMA_SPLIT_RE = re.compile(r'-|_')


class CalimaStarReinflector(object):
    """[summary]
    """

    def __init__(self, db):
        self._db = db
        self._analyzer = CalimaStarAnalyzer(db)
        self._generator = CalimaStarGenerator(db)

    def reinflect(self, word, feats):
        analyses = self._analyzer.analyze(word)

        if not analyses or len(analyses) == 0:
            return []

        for feat in feats:
            if feat not in self._db.defines:
                # FIXME: Throw exception instead
                # print('Feat key not in defines')
                return None
            elif (self._db.defines[feat] is not None and
                  feats[feat] not in self._db.defines[feat]):
                # print('Feat val not in defines')
                # FIXME: Throw exception instead
                return None

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
