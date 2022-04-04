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


from functools import reduce


__all__ = [
    'FEATS_10',
    'FEATS_14',
    'FEATS_16',
    'FEATURE_SET_MAP',
    'score_analysis_uniform'
]


# 10 features described in Khalifa et al., 2020
# Morphological Analysis and Disambiguation for Gulf Arabic: The Interplay
# between Resources and Methods
FEATS_10 = [
    'pos', 'per', 'form_gen', 'form_num', 'asp', 'prc0', 'prc1', 'prc2',
    'prc3', 'enc0'
]

FEATS_14 = [
    'pos', 'per', 'form_gen', 'form_num', 'asp', 'mod', 'vox', 'stt', 'cas',
    'prc0', 'prc1', 'prc2', 'prc3', 'enc0'
]

FEATS_16 = [
    'pos', 'per', 'form_gen', 'form_num', 'asp', 'mod', 'vox', 'stt', 'cas',
    'prc0', 'prc1', 'prc2', 'prc3', 'enc0', 'enc1', 'enc2'
]

FEATURE_SET_MAP = {
    'feats_10': FEATS_10,
    'feats_14': FEATS_14,
    'feats_16': FEATS_16,
}


def score_analysis_uniform(analysis, reference, mle_model=None,
                           tie_breaker=None, features=FEATS_16):
    """Calculate the score of matches given the predictions from the classifier
    and the analyses from the morphological analyzer.
    """

    # for GLF and LEV analyzers that use num for form_num, and gen for form_gen
    if 'form_num' not in analysis.keys():
        analysis['form_num'] = analysis['num']
    if 'form_gen' not in analysis.keys():
        analysis['form_gen'] = analysis['gen']

    score = sum(
        analysis.get(feat, '') == reference.get(feat, '') for feat in features
    )

    if tie_breaker == 'tag':
        score += _tie_breaker_tag(analysis, reference, mle_model)

    return score


def _tie_breaker_tag(analysis, reference, mle_model):
    """Calculate the tie breaker score using factored tag and unfactored tag
    probabilities in the training data.
    """

    ordered_feats = mle_model['info']['features']
    score_factored_tag = reduce(lambda x, y: x*y,
                                [mle_model[x].get(analysis.get(x, ''), 0)
                                for x in ordered_feats])
    unfactored_tag = ' '.join(
        f'{x}:{analysis.get(x, "")}' for x in ordered_feats
    )

    score_unfactored_tag = mle_model['unfactored'].get(unfactored_tag, 0)

    return (score_factored_tag + score_unfactored_tag) / 2