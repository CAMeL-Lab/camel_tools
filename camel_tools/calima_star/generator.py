# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018 New York University Abu Dhabi
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

"""The generator component of CALIMA Star.
"""

from __future__ import absolute_import

import copy
import collections

from camel_tools.calima_star.database import CalimaStarDB
from camel_tools.calima_star.errors import GeneratorError
from camel_tools.calima_star.errors import InvalidGeneratorFeature
from camel_tools.calima_star.errors import InvalidGeneratorFeatureValue
from camel_tools.calima_star.utils import merge_features


class CalimaStarGenerator(object):
    """CALIMA Star generator component.

    Args:
        db (:obj:`~camel_tools.calima_star.database.CalimaStarDB`): Database to
            use for generation. Must be opened in generation or reinflection
            mode.

    Raises:
        :obj:`~camel_tools.calima_star.errors.GeneratorError`: If **db** is not
            an instance of
            :obj:`~camel_tools.calima_star.database.CalimaStarDB` or if **db**
            does not support generation.
    """

    def __init__(self, db):
        if not isinstance(db, CalimaStarDB):
            raise GeneratorError('DB is not an instance of CalimaStarDB')
        if not db.flags.generation:
            raise GeneratorError('DB does not support generation')

        self._db = db

    def generate(self, lemma, feats):
        """Generate analyses for a given lemma and a given set of features.

        Args:
            lemma (:obj:`str`): Lemma to generate from.
            feats (:obj:`dict`): Dictionary of features. Must contain 'pos'
                feature.
                See :doc:`/reference/calima_star_features` for more information
                on features and their values.

        Returns:
            :obj:`list` of :obj:`dict`: List of generated analyses.
            See :doc:`/reference/calima_star_features` for more information on
            features and their values.

        Raises:
            :obj:`~camel_tools.calima_star.errors.InvalidGeneratorFeature`: If
                a feature is given that is not defined in database.
            :obj:`~camel_tools.calima_star.errors.InvalidGeneratorFeatureValue`:
                If an invalid value is given to a feature or if 'pos' feature
                is not defined.
        """

        if lemma not in self._db.lemma_hash:
            return []

        for feat in feats:
            if feat not in self._db.defines:
                raise InvalidGeneratorFeature(feat)
            elif (self._db.defines[feat] is not None and
                  feats[feat] not in self._db.defines[feat]):
                raise InvalidGeneratorFeatureValue(feat, feats[feat])

        if 'pos' not in feats or feats['pos'] not in self._db.defines['pos']:
            raise InvalidGeneratorFeatureValue('pos', feats.get('pos', None))

        feats = copy.copy(feats)

        default = self._db.defaults[feats['pos']]
        default_feat_set = frozenset(default.keys())
        feat_set = frozenset(feats.keys())

        if not feat_set.issubset(default_feat_set):
            return []

        # Set default values for undefined feats
        for feat in ['prc0', 'prc1', 'prc2', 'prc3', 'enc0']:
            if feat not in feats and feat in default:
                feats[feat] = default[feat]

        stem_feats_list = self._db.lemma_hash[lemma]
        analyses = collections.deque()

        for stem_feats in stem_feats_list:

            if 'vox' in feats and stem_feats['vox'] != feats['vox']:
                continue
            if 'rat' in feats and stem_feats['rat'] != feats['rat']:
                continue
            if 'pos' in feats and stem_feats['pos'] != feats['pos']:
                continue

            ignore_stem = False
            for feat in ['prc0', 'prc1', 'prc2', 'prc3', 'enc0']:
                if feat not in feats:
                    continue
                if (feat in stem_feats and
                        stem_feats[feat] != '0' and
                        feats[feat] != stem_feats[feat]):
                    ignore_stem = True
                    break

            if ignore_stem:
                continue

            prefix_cats = self._db.stem_prefix_compat[stem_feats['stemcat']]
            suffix_cats = self._db.stem_suffix_compat[stem_feats['stemcat']]

            for prefix_cat in prefix_cats:
                if prefix_cat not in self._db.prefix_cat_hash:
                    continue

                prefix_feats_list = self._db.prefix_cat_hash[prefix_cat]
                for prefix_feats in prefix_feats_list:
                    ignore_prefix = False

                    for feat in ['prc0', 'prc1', 'prc2', 'prc3']:
                        if feat not in feats:
                            continue
                        if ((feats[feat] != '0' and
                             feat not in prefix_feats and
                             stem_feats.get(feat, '0') != feats[feat]) or
                            (feat in prefix_feats and
                             feats[feat] != prefix_feats[feat])):
                            ignore_prefix = True
                            break

                    if ignore_prefix:
                        continue

                    for suffix_cat in suffix_cats:
                        if suffix_cat not in self._db.suffix_cat_hash:
                            continue
                        suffix_feats_list = (
                            self._db.suffix_cat_hash[suffix_cat])
                        for suffix_feats in suffix_feats_list:
                            if ((prefix_cat not in
                                 self._db.prefix_suffix_compat) or
                                (suffix_cat not in
                                 self._db.prefix_suffix_compat[prefix_cat])):
                                continue

                            ignore_suffix = False

                            for feat in ['enc0']:
                                if feat not in feats:
                                    continue
                                if ((feats[feat] != '0' and
                                     feat not in suffix_feats and
                                     stem_feats.get(feat, '0') != feats[feat])
                                    or (feat in suffix_feats and
                                        feats[feat] != suffix_feats[feat])):
                                    ignore_suffix = True
                                    break

                            if ignore_suffix:
                                continue

                            merged = merge_features(self._db, prefix_feats,
                                                    stem_feats, suffix_feats)

                            ignore_analysis = False
                            for feat in feats.keys():
                                if (feat in merged and
                                        merged[feat] != feats[feat]):
                                    ignore_analysis = True
                                    break

                            if not ignore_analysis:
                                analyses.append(merged)

        return list(analyses)
