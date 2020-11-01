# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2020 New York University Abu Dhabi
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


"""Contains a disambiguator that uses a Maximum Likelihood Estimation model.
"""


import json

from cachetools import LFUCache, cached
import editdistance

from camel_tools.utils.dediac import dediac_ar
from camel_tools.disambig.common import Disambiguator, DisambiguatedWord
from camel_tools.disambig.common import ScoredAnalysis
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.data import DataCatalogue


def _calima_msa_r13_analyzer():
    db = MorphologyDB.builtin_db('calima-msa-r13', 'a')
    analyzer = Analyzer(db, 'NOAN_PROP')
    return analyzer


def _calima_egy_r13_analyzer():
    db = MorphologyDB.builtin_db('calima-egy-r13', 'a')
    analyzer = Analyzer(db, 'NOAN_PROP')
    return analyzer


_MLE_ANALYZER_MAP = {
    'calima-msa-r13': _calima_msa_r13_analyzer,
    'calima-egy-r13': _calima_egy_r13_analyzer
}


def _get_pos_lex_logprob(analysis):
    logprob = analysis.get('pos_lex_logprob', -99.0)
    if logprob is None:
        return -99
    return logprob


_EQ_FEATS = frozenset(['asp', 'cas', 'enc0', 'gen', 'mod', 'num', 'per', 'pos',
                       'prc0', 'prc1', 'prc2', 'prc3', 'form_num', 'form_gen',
                       'enc1', 'enc2', 'stt', 'vox'])
_DISTANCE_FEATS = frozenset(['diac', 'lex', 'bw'])


def _score_analysis(analysis, reference):
    score = 0.0

    for feat in _EQ_FEATS:
        if analysis.get(feat, '') == reference.get(feat, ''):
            score += 1

    for feat in _DISTANCE_FEATS:
        feat_r = reference.get(feat, '')
        feat_a = analysis.get(feat, '')
        distance = editdistance.eval(feat_r, feat_a)
        score += max(0.0, (len(feat_r) - distance) / len(feat_r))

    return score


class MLEDisambiguator(Disambiguator):
    """A disambiguator using a Maximum Likelihood Estimation (MLE) model.
    It first does a lookup in a given word-based MLE model. If none is provided
    or a word is not in the word-based model, then an analyzer is used to
    disambiguate words based on the pos-lex log probabilities of their analyses.

    Args:
        analyzer (:obj:`~camel_tools.morphology.analyzer.Analyzer`):
            Disambiguator to use if a word is not in the word-based MLE model.
            The analyzer should provide the pos-lex log probabilities for
            analyses to disambiguate analyses.
        mle_path (:obj:`str`, optional): Path to MLE JSON file. If `None`,
            then no word-based MLE lookup is performed skipping directly to
            using the pos-lex model. Defaults to `None`.
        top (:obj:`int`, optional): The maximum number of top analyses to
            return. Defaults to 1.
        cache_size (:obj:`int`, optional): The number of unique word
            disambiguations to cache. The cache uses a least-frequently-used
            eviction policy. Defaults to 100000.
    """

    def __init__(self, analyzer, mle_path=None, top=1, cache_size=100000):
        if not isinstance(analyzer, Analyzer):
            raise ValueError('Invalid analyzer instance.')
        if not isinstance(top, int):
            raise ValueError('Invalid value for top.')
        if not isinstance(cache_size, int):
            raise ValueError('Invalid value for cache_size.')

        if mle_path is not None:
            with open(mle_path, 'r', encoding='utf-8') as mle_fp:
                self._mle = json.load(mle_fp)
        else:
            self._mle = None

        self._analyzer = analyzer

        if top < 1:
            top = 1
        self._top = top

        if cache_size < 0:
            cache_size = 0

        self._cache = LFUCache(cache_size)
        self._scored_analyses = cached(self._cache)(
            self._scored_analyses)

    @staticmethod
    def pretrained(model_name=None, analyzer=None, top=1, cache_size=100000):
        """Load a pre-trained MLE disambiguator provided with CAMeL Tools.

        Args:
            model_name (:obj:`str`, optional): The name of the pretrained
                model. If none, the default model ('calima-msa-r13') is loaded.
                At the moment, the model names available are the same as those
                in :ref:`camel_morphology_dbs`.
                Defaults to None.
            analyzer (:obj:`Analyzer`, optional): Alternative
                analyzer to use. If None, an instance of the model's default
                analyzer is created. Defaults to None.
            top (:obj:`int`, optional): The maximum number of top analyses to
                return. Defaults to 1.
            cache_size (:obj:`int`, optional): The number of unique word
                disambiguations to cache. The cache uses a
                least-frequently-used eviction policy. Defaults to 100000.

        Returns:
            :obj:`MLEDisambiguator`: The loaded MLE disambiguator.
        """

        model_info = DataCatalogue.get_dataset_info('DisambigMLE', model_name)
        mle_path = model_info.path / 'model.json'

        if analyzer is None:
            analyzer = _MLE_ANALYZER_MAP[model_info.name]()

        return MLEDisambiguator(analyzer, str(mle_path), top, cache_size)

    def _scored_analyses(self, word_dd):
        if self._mle is not None and word_dd in self._mle:
            mle_analysis = self._mle[word_dd]
            analyses = self._analyzer.analyze(word_dd)

            if len(analyses) == 0:
                return []

            scored = [(_score_analysis(a, mle_analysis), a) for a in analyses]
            scored.sort(key=lambda s: (-s[0], len(s[1]['bw']), s[1]['diac']))

            max_score = max([s[0] for s in scored])

            scored_analyses = [ScoredAnalysis(s[0] / max_score, s[1])
                               for s in scored]

            return scored_analyses[0:self._top]

        else:
            analyses = self._analyzer.analyze(word_dd)

            if len(analyses) == 0:
                return []

            probabilities = [10 ** _get_pos_lex_logprob(a) for a in analyses]
            max_prob = max(probabilities)

            scored_analyses = [ScoredAnalysis(p / max_prob, a)
                               for a, p in zip(analyses, probabilities)]
            scored_analyses.sort(key=lambda w: (-w.score,
                                                len(w.analysis['bw']),
                                                w.analysis['diac']))

            return scored_analyses[0:self._top]

    def _disambiguate_word(self, word):
        word_dd = dediac_ar(word)
        scored_analyses = self._scored_analyses(word_dd)

        return DisambiguatedWord(word, scored_analyses)

    def disambiguate_word(self, sentence, word_ndx):
        """Disambiguates a single word in a sentence. Note, that while MLE
        disambiguation operates on each word out of context, we maintain this
        interface to be compatible with disambiguators that work in context
        of a sentence.

        Args:
            sentence (:obj:`list` of :obj:`str`): The list of space and
                punctuation seperated list of tokens comprising a given
                sentence.
            word_ndx (:obj:`int`): The index of the word token in `sentence` to
                disambiguate.

        Returns:
            :obj:`~camel_tools.disambig.common.DisambiguatedWord`: The
            disambiguation of the word token in `sentence` at `word_ndx`.
        """

        return self._disambiguate_word(sentence[word_ndx])

    def disambiguate(self, sentence):
        """Disambiguate all words in a given sentence.

        Args:
            sentence (:obj:`list` of :obj:`str`): The list of space and
                punctuation seperated list of tokens comprising a given
                sentence.

        Returns:
            :obj:`list` of :obj:`~camel_tools.disambig.common.DisambiguatedWord`:
            The list of disambiguations for each word in the given sentence.
        """

        return [self._disambiguate_word(w) for w in sentence]
