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


import json
from pathlib import Path
import pickle

from cachetools import LFUCache
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from transformers import BertForTokenClassification, BertTokenizer

from camel_tools.data import CATALOGUE
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.disambig.common import Disambiguator, DisambiguatedWord
from camel_tools.disambig.common import ScoredAnalysis
from camel_tools.disambig.bert._bert_morph_dataset import MorphDataset
from camel_tools.disambig.score_function import score_analysis_uniform
from camel_tools.disambig.score_function import FEATURE_SET_MAP


_SCORING_FUNCTION_MAP = {
    'uniform': score_analysis_uniform
}


def _read_json(f_path):
    with open(f_path) as f:
        return json.load(f)


class _BERTFeatureTagger:
    """A feature tagger based on the fine-tuned BERT architecture.

        Args:
            model_path (:obj:`str`): The path to the fine-tuned model.
            use_gpu (:obj:`bool`, optional): The flag to use a GPU or not.
                Defaults to True.
    """

    def __init__(self, model_path, use_gpu=True):
        self._model = BertForTokenClassification.from_pretrained(model_path)
        self._tokenizer = BertTokenizer.from_pretrained(model_path)
        self._labels_map = self._model.config.id2label
        self._use_gpu = use_gpu

    def labels(self):
        """Get the list of Morph labels returned by predictions.

        Returns:
            :obj:`list` of :obj:`str`: List of Morph labels.
        """

        return list(self._labels_map.values())

    def _align_predictions(self, predictions, label_ids, sent_ids):
        """Aligns the predictions of the model with the inputs and it takes
        care of getting rid of the padding token.

        Args:
            predictions (:obj:`np.ndarray`): The predictions of the model
            label_ids (:obj:`np.ndarray`): The label ids of the inputs.
                They will always be the ids of Os since we're dealing with a
                test dataset. Note that label_ids are also padded.
            sent_ids (:obj:`np.ndarray`): The sent ids of the inputs.

        Returns:
            :obj:`list` of :obj:`list` of :obj:`str`: The predicted labels for
            all the sentences in the batch
        """

        preds = np.argmax(predictions, axis=2)
        batch_size, seq_len = preds.shape
        preds_list = [[] for _ in range(batch_size)]

        for i in range(batch_size):
            for j in range(seq_len):
                if label_ids[i, j] != nn.CrossEntropyLoss().ignore_index:
                    preds_list[i].append(self._labels_map[preds[i][j]])

        # Collating the predicted labels based on the sentence ids
        final_preds_list = [[] for _ in range(len(set(sent_ids)))]
        for i, id in enumerate(sent_ids):
            id = id - sent_ids[0]
            final_preds_list[id].extend(preds_list[i])

        return final_preds_list

    def predict(self, sentences, batch_size=32, max_seq_length=512):
        """Predict the morphosyntactic labels of a list of sentences.

        Args:
            sentences (:obj:`list` of :obj:`list` of :obj:`str`): The input
                sentences.
            batch_size (:obj:`int`): The batch size.
            max_seq_length (:obj:`int`): The max sequence size.

        Returns:
            :obj:`list` of :obj:`list` of :obj:`str`: The predicted
            morphosyntactic labels for the given sentences.
        """

        if len(sentences) == 0:
            return []

        sorted_sentences = list(enumerate(sentences))
        sorted_sentences = sorted(sorted_sentences, key=lambda x: len(x[1]))
        sorted_sentences_idx = [i[0] for i in sorted_sentences]
        sorted_sentences_text = [i[1] for i in sorted_sentences]

        test_dataset = MorphDataset(sentences=sorted_sentences_text,
                                    tokenizer=self._tokenizer,
                                    labels=list(self._labels_map.values()),
                                    max_seq_length=max_seq_length)

        data_loader = DataLoader(test_dataset, batch_size=batch_size,
                                 shuffle=False, drop_last=False,
                                 collate_fn=self._collate_fn)

        predictions = []
        device = ('cuda' if self._use_gpu and torch.cuda.is_available()
                  else 'cpu')
        self._model.to(device)
        self._model.eval()

        with torch.no_grad():
            for batch in data_loader:
                batch = {k: v.to(device) for k, v in batch.items()}
                inputs = {'input_ids': batch['input_ids'],
                          'token_type_ids': batch['token_type_ids'],
                          'attention_mask': batch['attention_mask']}

                label_ids = batch['label_ids']
                sent_ids = batch['sent_id']
                logits = self._model(**inputs)[0]
                preds = logits
                prediction = self._align_predictions(preds.cpu().numpy(),
                                                     label_ids.cpu().numpy(),
                                                     sent_ids.cpu().numpy())
                predictions.extend(prediction)

        sorted_predictions_pair = zip(sorted_sentences_idx, predictions)
        sorted_predictions = sorted(sorted_predictions_pair,
                                    key=lambda x: x[0])

        return [i[1] for i in sorted_predictions]

    def _collate_fn(self, batch):
        input_ids = []
        token_type_ids = []
        attention_mask = []
        label_ids = []
        sent_id = []

        # Find max length within the batch
        max_seq_length = 0
        for sent in batch:
            l = len(sent['input_ids'][sent['input_ids'].nonzero()].squeeze())
            max_seq_length = max(max_seq_length, l)

        # Truncate the unnecessary paddings
        for sent in batch:
            for _, t in sent.items():
                if _ != 'sent_id':
                    sent[_] = t[:max_seq_length]

        for sent in batch:
            input_ids.append(sent['input_ids'])
            token_type_ids.append(sent['token_type_ids'])
            attention_mask.append(sent['attention_mask'])
            label_ids.append(sent['label_ids'])
            sent_id.append(sent['sent_id'])

        return {
            'input_ids': torch.stack(input_ids),
            'token_type_ids': torch.stack(token_type_ids),
            'attention_mask': torch.stack(attention_mask),
            'label_ids': torch.stack(label_ids),
            'sent_id': torch.tensor(sent_id, dtype=torch.int32),
        }


class BERTUnfactoredDisambiguator(Disambiguator):
    """A disambiguator using an unfactored BERT model. This model is based on
    *Morphosyntactic Tagging with Pre-trained Language Models for Arabic and
    its Dialects* by Inoue, Khalifa, and Habash. Findings of ACL 2022.
    (https://arxiv.org/abs/2110.06852)

    Args:
        model_path (:obj:`str`): The path to the fine-tuned model.
        analyzer (:obj:`~camel_tools.morphology.analyzer.Analyzer`): Analyzer
            to use for providing full morphological analysis of a word.
        features: :obj:`list`, optional): A list of morphological features
            used in the model. Defaults to 14 features.
        top (:obj:`int`, optional): The maximum number of top analyses to
            return. Defaults to 1.
        scorer (:obj:`str`, optional): The scoring function that computes
            matches between the predicted features from the model and the
            output from the analyzer. If `uniform`, the scoring based on the
            uniform weight is used. Defaults to `uniform`.
        tie_breaker (:obj:`str`, optional): The tie breaker used in the feature
            match function. If `tag`, tie breaking based on the unfactored tag
            MLE and factored tag MLE is used. Defaults to `tag`.
        use_gpu (:obj:`bool`, optional): The flag to use a GPU or not.
            Defaults to True.
        batch_size (:obj:`int`, optional): The batch size. Defaults to 32.
        ranking_cache (:obj:`LFUCache`, optional): The cache of pre-computed
            scored analyses. Defaults to `None`.
        ranking_cache_size (:obj:`int`, optional): The number of unique word
            disambiguations to cache. If 0, no ranked analyses will be cached.
            The cache uses a least-frequently-used eviction policy.
            Defaults to 100000.
    """

    def __init__(self, model_path, analyzer,
                 features=FEATURE_SET_MAP['feats_14'], top=1,
                 scorer='uniform', tie_breaker='tag', use_gpu=True,
                 batch_size=32, ranking_cache=None, ranking_cache_size=100000):
        self._model = {
            'unfactored': _BERTFeatureTagger(model_path)
        }
        self._analyzer = analyzer
        self._features = features
        self._top = max(top, 1)
        self._scorer = _SCORING_FUNCTION_MAP.get(scorer, None)
        self._tie_breaker = tie_breaker
        self._use_gpu = use_gpu
        self._batch_size = batch_size
        self._mle = _read_json(f'{model_path}/mle_model.json')

        if ranking_cache is None:
            if ranking_cache_size <= 0:
                self._ranking_cache = None
                self._disambiguate_word_fn = self._disambiguate_word
            else:
                self._ranking_cache = LFUCache(ranking_cache_size)
                self._disambiguate_word_fn = self._disambiguate_word_cached
        else:
            self._ranking_cache = ranking_cache
            self._disambiguate_word_fn = self._disambiguate_word_cached

    @staticmethod
    def pretrained(model_name='msa', top=1, use_gpu=True, batch_size=32,
                   cache_size=10000, pretrained_cache=True,
                   ranking_cache_size=100000):
        """Load a pre-trained model provided with camel_tools.

        Args:
            model_name (:obj:`str`, optional): Name of pre-trained model to
                load. Three models are available: 'msa', 'egy', and 'glf.
                Defaults to `msa`.
            top (:obj:`int`, optional): The maximum number of top analyses to
                return. Defaults to 1.
            use_gpu (:obj:`bool`, optional): The flag to use a GPU or not.
                Defaults to True.
            batch_size (:obj:`int`, optional): The batch size. Defaults to 32.
            cache_size (:obj:`int`, optional): If greater than zero, then
                the analyzer will cache the analyses for the cache_size most
                frequent words, otherwise no analyses will be cached.
                Defaults to 100000.
            pretrained_cache (:obj:`bool`, optional): The flag to use a
                    pretrained cache that stores ranked analyses.
                    Defaults to True.
            ranking_cache_size (:obj:`int`, optional): The number of unique
                word disambiguations to cache. If 0, no ranked analyses will be
                cached. The cache uses a least-frequently-used eviction policy.
                This argument is ignored if pretrained_cache is True.
                Defaults to 100000.

        Returns:
            :obj:`BERTUnfactoredDisambiguator`: Instance with loaded
            pre-trained model.
        """

        model_info = CATALOGUE.get_dataset('DisambigBertUnfactored',
                                           model_name)
        model_config = _read_json(Path(model_info.path, 'default_config.json'))
        model_path = str(model_info.path)
        features = FEATURE_SET_MAP[model_config['feature']]
        db = MorphologyDB.builtin_db(model_config['db_name'], 'a')
        analyzer = Analyzer(db, backoff=model_config['backoff'],
                            cache_size=cache_size)
        scorer = model_config['scorer']
        tie_breaker = model_config['tie_breaker']
        if pretrained_cache:
            cache_info = CATALOGUE.get_dataset('DisambigRankingCache',
                                               model_config['ranking_cache'])
            cache_path = Path(cache_info.path, 'default_cache.pickle')
            with open(cache_path, 'rb') as f:
                ranking_cache = pickle.load(f)
        else:
            ranking_cache = None

        return BERTUnfactoredDisambiguator(
            model_path,
            analyzer,
            top=top,
            features=features,
            scorer=scorer,
            tie_breaker=tie_breaker,
            use_gpu=use_gpu,
            batch_size=batch_size,
            ranking_cache=ranking_cache,
            ranking_cache_size=ranking_cache_size)

    @staticmethod
    def _pretrained_from_config(config, top=1, use_gpu=True, batch_size=32,
                               cache_size=10000, pretrained_cache=True,
                               ranking_cache_size=100000):
        """Load a pre-trained model from a config file.

        Args:
            config (:obj:`str`): Config file that defines the model details.
                Defaults to `None`.
            top (:obj:`int`, optional): The maximum number of top analyses
                to return. Defaults to 1.
            use_gpu (:obj:`bool`, optional): The flag to use a GPU or not.
                Defaults to True.
            batch_size (:obj:`int`, optional): The batch size. Defaults to 32.
            cache_size (:obj:`int`, optional): If greater than zero, then
                the analyzer will cache the analyses for the cache_size
                most frequent words, otherwise no analyses will be cached.
                Defaults to 100000.
            pretrained_cache (:obj:`bool`, optional): The flag to use a
                pretrained cache that stores ranked analyses.
                Defaults to True.
            ranking_cache_size (:obj:`int`, optional): The number of unique
                word disambiguations to cache. If 0, no ranked analyses will be
                cached. The cache uses a least-frequently-used eviction policy.
                This argument is ignored if pretrained_cache is True.
                Defaults to 100000.

        Returns:
            :obj:`BERTUnfactoredDisambiguator`: Instance with loaded
            pre-trained model.
        """

        model_config = _read_json(config)
        model_path = model_config['model_path']
        features = FEATURE_SET_MAP[model_config['feature']]
        db = MorphologyDB(model_config['db_path'], 'a')
        analyzer = Analyzer(db,
                            backoff=model_config['backoff'],
                            cache_size=cache_size)
        scorer = model_config['scorer']
        tie_breaker = model_config['tie_breaker']
        if pretrained_cache:
            cache_path = model_config['ranking_cache']
            with open(cache_path, 'rb') as f:
                ranking_cache = pickle.load(f)
        else:
            ranking_cache = None

        return BERTUnfactoredDisambiguator(
            model_path,
            analyzer,
            top=top,
            features=features,
            scorer=scorer,
            tie_breaker=tie_breaker,
            use_gpu=use_gpu,
            batch_size=batch_size,
            ranking_cache=ranking_cache,
            ranking_cache_size=ranking_cache_size)

    def _predict_sentences(self, sentences):
        """Predict the morphosyntactic labels of a list of sentences.

        Args:
            sentences (:obj:`list` of :obj:`list` of :obj:`str`): The input
                sentences.

        Returns:
            :obj:`list` of :obj:`list` of :obj:`dict`: The predicted
            morphosyntactic labels for the given sentences.
        """

        preds = self._model['unfactored'].predict(sentences, self._batch_size)
        parsed_predictions = []

        for sent, pred in zip(sentences, preds):
            parsed_prediction = []

            for word, pred in zip(sent, pred):
                d = {}
                for feat in pred.split('__'):
                    f, v = feat.split(':')
                    d[f] = v

                d['lex'] = word  # Copy the word when analyzer is not used
                d['diac'] = word  # Copy the word when analyzer is not used

                parsed_prediction.append(d)

            parsed_predictions.append(parsed_prediction)

        return parsed_predictions

    def _predict_sentence(self, sentence):
        """Predict the morphosyntactic labels of a single sentence.

        Args:
            sentence (:obj:`list` of :obj:`str`): The input sentence.

        Returns:
            :obj:`list` of :obj:`dict`: The predicted morphosyntactic labels
            for the given sentence.
        """

        parsed_predictions = []
        model = self._model['unfactored']
        preds =  model.predict([sentence], self._batch_size)[0]

        for word, pred in zip(sentence, preds):
            d = {}
            for feat in pred.split('__'):
                f, v = feat.split(':')
                d[f] = v

            d['lex'] = word  # Copy the word when analyzer is not used
            d['diac'] = word  # Copy the word when analyzer is not used

            parsed_predictions.append(d)

        return parsed_predictions

    def _scored_analyses(self, word_dd, prediction):
        bert_analysis = prediction
        analyses = self._analyzer.analyze(word_dd)

        if len(analyses) == 0:
            # If the word is not found in the analyzer,
            # return the predictions from BERT
            return [ScoredAnalysis(0, bert_analysis)]

        scored = [(self._scorer(a,
                                bert_analysis,
                                self._mle,
                                tie_breaker=self._tie_breaker,
                                features=self._features), a)
                  for a in analyses]
        scored.sort(key=lambda s: (-s[0], s[1]['diac']))

        max_score = max(s[0] for s in scored)

        if max_score != 0:
            scored_analyses = [ScoredAnalysis(s[0] / max_score, s[1])
                               for s in scored]
        else:
            # If the max score is 0, do not divide
            scored_analyses = [ScoredAnalysis(0, s[1]) for s in scored]

        return scored_analyses[:self._top]

    def _disambiguate_word(self, word, pred):
        scored_analyses = self._scored_analyses(word, pred)

        return DisambiguatedWord(word, scored_analyses)

    def _disambiguate_word_cached(self, word, pred):
        # Create a key for caching scored analysis given word and bert
        # predictions
        key = (word, tuple(pred[feat] for feat in self._features))

        if key in self._ranking_cache:
            scored_analyses = self._ranking_cache[key]
        else:
            scored_analyses = self._scored_analyses(word, pred)
            self._ranking_cache[key] = scored_analyses

        return DisambiguatedWord(word, scored_analyses)

    def disambiguate_word(self, sentence, word_ndx):
        """Disambiguates a single word of a sentence.

        Args:
            sentence (:obj:`list` of :obj:`str`): The input sentence.
            word_ndx (:obj:`int`): The index of the word token in `sentence` to
                disambiguate.

        Returns:
            :obj:`~camel_tools.disambig.common.DisambiguatedWord`: The
            disambiguation of the word token in `sentence` at `word_ndx`.
        """

        return self.disambiguate(sentence)[word_ndx]

    def disambiguate(self, sentence):
        """Disambiguate all words of a single sentence.

        Args:
            sentence (:obj:`list` of :obj:`str`): The input sentence.

        Returns:
            :obj:`list` of :obj:`~camel_tools.disambig.common.DisambiguatedWord`: The
            disambiguated analyses for the given sentence.
        """

        predictions = self._predict_sentence(sentence)

        return [self._disambiguate_word_fn(w, p)
                for (w, p) in zip(sentence, predictions)]

    def disambiguate_sentences(self, sentences):
        """Disambiguate all words of a list of sentences.
        
        Args:
            sentences (:obj:`list` of :obj:`list` of :obj:`str`): The input
                sentences.

        Returns:
            :obj:`list` of :obj:`list` of :obj:`~camel_tools.disambig.common.DisambiguatedWord`: The
            disambiguated analyses for the given sentences.
        """

        predictions = self._predict_sentences(sentences)
        disambiguated_sentences = []

        for sentence, prediction in zip(sentences, predictions):
            disambiguated_sentence = [
                self._disambiguate_word_fn(w, p)
                for (w, p) in zip(sentence, prediction)
            ]
            disambiguated_sentences.append(disambiguated_sentence)

        return disambiguated_sentences

    def tag_sentences(self, sentences, use_analyzer=True):
        """Predict the morphosyntactic labels of a list of sentences. 

        Args:
            sentences (:obj:`list` of :obj:`list` of :obj:`str`): The input
                sentences.
            use_analyzer (:obj:`bool`): The flag to use an analyzer or not.
                If set to False, we return the original input as diac and lex.
                Defaults to True.

        Returns:
            :obj:`list` of :obj:`list` of :obj:`dict`: The predicted The list
            of feature tags for each word in the given sentences
        """

        if use_analyzer:
            tagged_sentences = []
            for prediction in self.disambiguate_sentences(sentences):
                tagged_sentence = [a.analyses[0].analysis for a in prediction]
                tagged_sentences.append(tagged_sentence)

            return tagged_sentences

        return self._predict_sentences(sentences)

    def tag_sentence(self, sentence, use_analyzer=True):
        """Predict the morphosyntactic labels of a single sentence. 

        Args:
            sentence (:obj:`list` of :obj:`str`): The list of space and
                punctuation seperated list of tokens comprising a given
                sentence.
            use_analyzer (:obj:`bool`): The flag to use an analyzer or not.
                If set to False, we return the original input as diac and lex.
                Defaults to True.

        Returns:
            :obj:`list` of :obj:`dict`: The list of feature tags for each word
            in the given sentence
        """

        if use_analyzer:
            return [a.analyses[0].analysis
                    for a in self.disambiguate(sentence)]

        return self._predict_sentence(sentence)

    def all_feats(self):
        """Return a set of all features produced by this disambiguator.

        Returns:
            :obj:`frozenset` of :obj:`str`: The set all features produced by
            this disambiguator.
        """

        return self._analyzer.all_feats()

    def tok_feats(self):
        """Return a set of tokenization features produced by this
        disambiguator.

        Returns:
            :obj:`frozenset` of :obj:`str`: The set tokenization features
            produced by this disambiguator.
        """

        return self._analyzer.tok_feats()
