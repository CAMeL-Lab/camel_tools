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


"""This module contains the CAMeL Tools dialect identification component.
"""


import collections
from pathlib import Path
import sys

if sys.platform == 'win32':
    raise ModuleNotFoundError(
        'camel_tools.dialectid is not available on Windows.')
else:
    import kenlm

import numpy as np
import pandas as pd
import scipy as sp
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import normalize
from sklearn.metrics import accuracy_score, f1_score, recall_score
from sklearn.metrics import precision_score
import dill

from camel_tools.data import get_dataset_path
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.utils.dediac import dediac_ar


_DEFAULT_LABELS = frozenset(['ALE', 'ALG', 'ALX', 'AMM', 'ASW', 'BAG', 'BAS',
                             'BEI', 'BEN', 'CAI', 'DAM', 'DOH', 'FES', 'JED',
                             'JER', 'KHA', 'MOS', 'MSA', 'MUS', 'RAB', 'RIY',
                             'SAL', 'SAN', 'SFX', 'TRI', 'TUN'])

_DEFAULT_LABELS_EXTRA = frozenset(['BEI', 'CAI', 'DOH', 'MSA', 'RAB', 'TUN'])

_LABEL_MAP = {
    'ALE': 'Aleppo',
    'ALG': 'Algiers',
    'ALX': 'Alexandria',
    'AMM': 'Amman',
    'ASW': 'Aswan',
    'BAG': 'Baghdad',
    'BAS': 'Basra',
    'BEI': 'Beirut',
    'BEN': 'Benghazi',
    'CAI': 'Cairo',
    'DAM': 'Damascus',
    'DOH': 'Doha',
    'FES': 'Fes',
    'JED': 'Jeddha',
    'JER': 'Jerusalem',
    'KHA': 'Khartoum',
    'MOS': 'Mosul',
    'MSA': 'Modern Standard Arabic',
    'MUS': 'Muscat',
    'RAB': 'Rabat',
    'RIY': 'Riyadh',
    'SAL': 'Salt',
    'SAN': 'Sana\'a',
    'SFX': 'Sfax',
    'TRI': 'Tripoli',
    'TUN': 'Tunis'
}

_DATA_DIR = get_dataset_path('DialectID')
_CHAR_LM_DIR = Path(_DATA_DIR, 'lm', 'char')
_WORD_LM_DIR = Path(_DATA_DIR, 'lm', 'word')
_TRAIN_DATA_PATH = Path(_DATA_DIR, 'corpus_26_train.tsv')
_TRAIN_DATA_EXTRA_PATH = Path(_DATA_DIR, 'corpus_6_train.tsv')
_VAL_DATA_PATH = Path(_DATA_DIR, 'corpus_26_val.tsv')
_TEST_DATA_PATH = Path(_DATA_DIR, 'corpus_26_test.tsv')


class DIDPred(collections.namedtuple('DIDPred', ['top', 'scores'])):
    """A named tuple containing dialect ID prediction results.

    Attributes:
        top (:obj:`str`): The dialect label with the highest score.
        scores (:obj:`dict`): A dictionary mapping each dialect label to it's
            computed score.
    """


class DialectIdError(Exception):
    """Base class for all CAMeL Dialect ID errors.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


class UntrainedModelError(DialectIdError):
    """Error thrown when attempting to use an untrained DialectIdentifier
    instance.
    """

    def __init__(self, msg):
        DialectIdError.__init__(self, msg)


class InvalidDataSetError(DialectIdError, ValueError):
    """Error thrown when an invalid data set name is given to eval.
    """

    def __init__(self, dataset):
        msg = ('Invalid data set name {}. Valid names are "TEST" and '
               '"VALIDATION"'.format(repr(dataset)))
        DialectIdError.__init__(self, msg)


class PretrainedModelError(DialectIdError):
    """Error thrown when attempting to load a pretrained model provided with
    camel-tools.
    """

    def __init__(self, msg):
        DialectIdError.__init__(self, msg)


def _normalize_lm_scores(scores):
    norm_scores = np.exp(scores)
    norm_scores = normalize(norm_scores)
    return norm_scores


def _word_to_char(txt):
    return ' '.join(list(txt.replace(' ', 'X')))


def _max_score(score_tups):
    max_score = -1
    max_dialect = None

    for dialect, score in score_tups:
        if score > max_score:
            max_score = score
            max_dialect = dialect

    return max_dialect


class DialectIdentifier(object):
    """A class for training, evaluating and running the dialect identification
    model described by Salameh et al. After initializing an instance, you must
    run the train method once before using it.

    Args:
        labels (:obj:`set` of :obj:`str`, optional): The set of dialect labels
            used in the training data in the main model.
            If None, the default labels are used.
            Defaults to None.
        labels_extra (:obj:`set` of :obj:`str`, optional): The set of dialect
            labels used in the training data in the extra features model.
            If None, the default labels are used.
            Defaults to None.
        char_lm_dir (:obj:`str`, optional): Path to the directory containing
            the character-based language models. If None, use the language
            models that come with this package. Defaults to None.
        word_lm_dir (:obj:`str`, optional): Path to the directory containing
            the word-based language models. If None, use the language models
            that come with this package. Defaults to None.
    """

    def __init__(self, labels=None,
                 labels_extra=None,
                 char_lm_dir=None,
                 word_lm_dir=None):
        if labels is None:
            labels = _DEFAULT_LABELS
        if labels_extra is None:
            labels_extra = _DEFAULT_LABELS_EXTRA
        if char_lm_dir is None:
            char_lm_dir = _CHAR_LM_DIR
        if word_lm_dir is None:
            word_lm_dir = _WORD_LM_DIR

        self._labels = labels
        self._labels_extra = labels_extra
        self._labels_sorted = sorted(labels)
        self._labels_extra_sorted = sorted(labels_extra)

        self._char_lms = collections.defaultdict(kenlm.Model)
        self._word_lms = collections.defaultdict(kenlm.Model)
        self._load_lms(char_lm_dir, word_lm_dir)

        self._is_trained = False

    def _load_lms(self, char_lm_dir, word_lm_dir):
        config = kenlm.Config()
        config.show_progress = False

        for label in self._labels:
            char_lm_path = Path(char_lm_dir, '{}.arpa'.format(label))
            word_lm_path = Path(word_lm_dir, '{}.arpa'.format(label))
            self._char_lms[label] = kenlm.Model(str(char_lm_path), config)
            self._word_lms[label] = kenlm.Model(str(word_lm_path), config)

    def _get_char_lm_scores(self, txt):
        chars = _word_to_char(txt)
        return np.array([self._char_lms[label].score(chars, bos=True, eos=True)
                         for label in self._labels_sorted])

    def _get_word_lm_scores(self, txt):
        return np.array([self._word_lms[label].score(txt, bos=True, eos=True)
                         for label in self._labels_sorted])

    def _get_lm_feats(self, txt):
        word_lm_scores = self._get_word_lm_scores(txt).reshape(1, -1)
        word_lm_scores = _normalize_lm_scores(word_lm_scores)
        char_lm_scores = self._get_char_lm_scores(txt).reshape(1, -1)
        char_lm_scores = _normalize_lm_scores(char_lm_scores)
        feats = np.concatenate((word_lm_scores, char_lm_scores), axis=1)
        return feats

    def _get_lm_feats_multi(self, sentences):
        feats_list = collections.deque()
        for sentence in sentences:
            feats_list.append(self._get_lm_feats(sentence))
        feats_matrix = np.array(feats_list)
        feats_matrix = feats_matrix.reshape((-1, 52))
        return feats_matrix

    def _prepare_sentences(self, sentences):
        tokenized = [' '.join(simple_word_tokenize(dediac_ar(s)))
                     for s in sentences]
        sent_array = np.array(tokenized)
        x_trans = self._feat_union.transform(sent_array)
        x_trans_extra = self._feat_union_extra.transform(sent_array)
        x_predict_extra = self._classifier_extra.predict_proba(x_trans_extra)
        x_lm_feats = self._get_lm_feats_multi(sentences)
        x_final = sp.sparse.hstack((x_trans, x_lm_feats, x_predict_extra))
        return x_final

    def train(self, data_path=None,
              data_extra_path=None,
              char_ngram_range=(1, 3),
              word_ngram_range=(1, 1),
              n_jobs=None):
        """Trains the model on a given data set.

        Args:
            data_path (:obj:`str`, optional): Path to main training data.
                If None, use the provided training data.
                Defaults to None.
            data_extra_path (:obj:`str`, optional): Path to extra features
                training data. If None,cuse the provided training data.
                Defaults to None.
            char_ngram_range (:obj:`tuple`, optional): The n-gram ranges to
                consider in the character-based language models.
                Defaults to (1, 3).
            word_ngram_range (:obj:`tuple`, optional): The n-gram ranges to
                consider in the word-based language models.
                Defaults to (1, 1).
            n_jobs (:obj:`int`, optional): The number of parallel jobs to use
                for computation. If None, then only 1 job is used.
                If -1 then all processors are used. Defaults to None.
        """

        if data_path is None:
            data_path = _TRAIN_DATA_PATH
        if data_extra_path is None:
            data_extra_path = _TRAIN_DATA_EXTRA_PATH

        # Load training data and extract
        train_data = pd.read_csv(data_path, sep='\t', index_col=0)
        train_data_extra = pd.read_csv(data_extra_path, sep='\t', index_col=0)

        x = train_data['ar'].values
        y = train_data['dialect'].values
        x_extra = train_data_extra['ar'].values
        y_extra = train_data_extra['dialect'].values

        # Build and train extra classifier
        self._label_encoder_extra = LabelEncoder()
        self._label_encoder_extra.fit(y_extra)
        y_trans = self._label_encoder_extra.transform(y_extra)

        word_vectorizer = TfidfVectorizer(lowercase=False,
                                          ngram_range=word_ngram_range,
                                          analyzer='word',
                                          tokenizer=lambda x: x.split(' '))
        char_vectorizer = TfidfVectorizer(lowercase=False,
                                          ngram_range=char_ngram_range,
                                          analyzer='char',
                                          tokenizer=lambda x: x.split(' '))
        self._feat_union_extra = FeatureUnion([('wordgrams', word_vectorizer),
                                               ('chargrams', char_vectorizer)])
        x_trans = self._feat_union_extra.fit_transform(x_extra)

        self._classifier_extra = OneVsRestClassifier(MultinomialNB(),
                                                     n_jobs=n_jobs)
        self._classifier_extra.fit(x_trans, y_trans)

        # Build and train main classifier
        self._label_encoder = LabelEncoder()
        self._label_encoder.fit(y)
        y_trans = self._label_encoder.transform(y)

        word_vectorizer = TfidfVectorizer(lowercase=False,
                                          ngram_range=word_ngram_range,
                                          analyzer='word',
                                          tokenizer=lambda x: x.split(' '))
        char_vectorizer = TfidfVectorizer(lowercase=False,
                                          ngram_range=char_ngram_range,
                                          analyzer='char',
                                          tokenizer=lambda x: x.split(' '))
        self._feat_union = FeatureUnion([('wordgrams', word_vectorizer),
                                         ('chargrams', char_vectorizer)])
        self._feat_union.fit(x)

        x_prepared = self._prepare_sentences(x)

        self._classifier = OneVsRestClassifier(MultinomialNB(), n_jobs=n_jobs)
        self._classifier.fit(x_prepared, y_trans)

        self._is_trained = True

    def eval(self, data_path=None, data_set='VALIDATION'):
        """Evaluate the trained model on a given data set.

        Args:
            data_path (:obj:`str`, optional): Path to an evaluation data set.
                If None, use one of the provided data sets instead.
                Defaults to None.
            data_set (:obj:`str`, optional): Name of the provided data set to
                use. This is ignored if data_path is not None. Can be either
                'VALIDATION' or 'TEST'. Defaults to 'VALIDATION'.

        Returns:
            :obj:`dict`: A dictionary mapping an evaluation metric to its
            computed value. The metrics used are accuracy, f1_micro, f1_macro,
            recall_micro, recall_macro, precision_micro and precision_macro.
        """

        if not self._is_trained:
            raise UntrainedModelError(
                'Can\'t evaluate an untrained model.')

        if data_path is None:
            if data_set == 'VALIDATION':
                data_path = _VAL_DATA_PATH
            elif data_set == 'TEST':
                data_path = _TEST_DATA_PATH
            else:
                raise InvalidDataSetError(data_set)

        # Load eval data
        eval_data = pd.read_csv(data_path, sep='\t', index_col=0)
        x = eval_data['ar'].values
        y_true = eval_data['dialect'].values

        # Generate predictions
        x_prepared = self._prepare_sentences(x)
        y_pred = self._classifier.predict(x_prepared)
        y_pred = self._label_encoder.inverse_transform(y_pred)

        # Get scores
        scores = {
            'accuracy': accuracy_score(y_true, y_pred),
            'f1_micro': f1_score(y_true, y_pred, average='micro'),
            'f1_macro': f1_score(y_true, y_pred, average='macro'),
            'recall_micro': recall_score(y_true, y_pred, average='micro'),
            'recall_macro': recall_score(y_true, y_pred, average='macro'),
            'precision_micro': precision_score(y_true, y_pred,
                                               average='micro'),
            'precision_macro': precision_score(y_true, y_pred, average='macro')
        }

        return scores

    def predict(self, sentences):
        """Predict the dialect probability scores for a given list of
        sentences.

        Args:
            sentences (:obj:`list` of :obj:`str`): The list of sentences.

        Returns:
            :obj:`list` of :obj:`DIDPred`: A list of prediction results,
            each corresponding to its respective sentence.
        """

        if not self._is_trained:
            raise UntrainedModelError(
                'Can\'t predict with an untrained model.')

        x_prepared = self._prepare_sentences(sentences)
        predicted_scores = self._classifier.predict_proba(x_prepared)

        result = collections.deque()
        for sentence, scores in zip(sentences, predicted_scores):
            score_tups = list(zip(self._labels_sorted, scores))
            predicted_dialect = _max_score(score_tups)
            dialect_scores = dict(score_tups)
            result.append(DIDPred(predicted_dialect, dialect_scores))

        return list(result)

    @staticmethod
    def pretrained():
        """Load the default pre-trained model provided with camel-tools.

        Raises:
            :obj:`PretrainedModelError`: When a pre-trained model compatible
                with the current Python version isn't available.

        Returns:
            :obj:`DialectIdentifier`: The loaded model.
        """

        suffix = '{}{}'.format(sys.version_info.major, sys.version_info.minor)
        model_file_name = 'did_pretrained_{}.dill'.format(suffix)
        model_path = Path(_DATA_DIR, model_file_name)

        if not model_path.is_file():
            raise PretrainedModelError(
                'No pretrained model for current Python version found.')

        with model_path.open('rb') as model_fp:
            model = dill.load(model_fp)

            # We need to reload LMs since they were set to None when
            # serialized.
            model._char_lms = collections.defaultdict(kenlm.Model)
            model._word_lms = collections.defaultdict(kenlm.Model)
            model._load_lms(_CHAR_LM_DIR, _WORD_LM_DIR)

            return model


def train_default_model():
    print(_DATA_DIR)
    did = DialectIdentifier()
    did.train()

    # We don't want to serialize kenlm models as they will utilize the
    # absolute LM paths used in training. They will be reloaded when using
    # DialectIdentifer.pretrained().
    did._char_lms = None
    did._word_lms = None

    suffix = '{}{}'.format(sys.version_info.major, sys.version_info.minor)
    model_file_name = 'did_pretrained_{}.dill'.format(suffix)
    model_path = Path(_DATA_DIR, model_file_name)

    with model_path.open('wb') as model_fp:
        dill.dump(did, model_fp)


def label_to_dialect(label):
    """Maps a given label from the default label set to the
    dialect the given label represents.

    Args:
        label (:obj:`str`): The input label.

    Returns:
        :obj:`str`: The dialect name associated with the input label. If the
        input label is not a valid label, None is returned instead.
    """

    return _LABEL_MAP.get(label, None)


def label_dialect_pairs():
    """Returns the set of default label-dialect pairs.

    Returns:
        :obj:`frozenset` of :obj:`tuple`: The set of default label-dialect
        pairs.
    """
    return frozenset(_LABEL_MAP.items())
