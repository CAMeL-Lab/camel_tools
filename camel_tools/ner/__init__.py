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


"""This module contains the CAMeL Tools Named Entity Recognition component.
"""


import torch
import torch.nn.functional as torch_fun
from transformers import BertTokenizer, BertForTokenClassification

from camel_tools.data import DataCatalogue


_LABELS = ['B-LOC', 'B-ORG', 'B-PERS', 'I-LOC', 'I-ORG', 'I-PERS']
_IGNORE_LABELS = []
_SPECIAL_TOKENS = ['[SEP]', '[CLS]']


class NERecognizer:
    """CAMeL Tools NER component.

    Args:
        model_path(:obj:`str`): The path to the fine-tuned model.
    """

    # TODO: Add options for custom values for special tokens
    def __init__(self, model_path):
        self.model = BertForTokenClassification.from_pretrained(model_path)
        self.tokenizer = BertTokenizer.from_pretrained(model_path,
                                                       do_basic_tokenize=False)
        self.labels_map = self.model.config.id2label

    @staticmethod
    def pretrained(model_name=None):
        """Load a pre-trained model provided with camel_tools.

        Args:
            model_name (:obj:`str`, optional): Name of pre-trained model to
                load.
                One model is available: 'arabert'.
                If None, the default model ('arabert') will be loaded.
                Defaults to None.

        Returns:
            :obj:`NERecognizer`: Instance with loaded pre-trained model.
        """

        model_info = DataCatalogue.get_dataset_info('NamedEntityRecognition',
                                                    model_name)
        model_path = str(model_info.path)

        return NERecognizer(model_path)

    @staticmethod
    def labels():
        """Get the list of NER labels returned by predictions.

        Returns:
            :obj:`list` of :obj:`str`: List of NER labels.
        """

        return list(_LABELS)

    def predict_sentence(self, sentence):
        """Predict the named entity labels of a single sentence.

        Args:
            sentence (:obj:`list` of :obj:`str`): The input sentence.

        Returns:
            :obj:`list` of :obj:`str`: The predicted named entity
            labels for the given sentence.
        """

        # Add special tokens takes care of adding [CLS], [SEP] tokens
        input_ids = torch.tensor(
            self.tokenizer.encode(sentence, add_special_tokens=True,
                                  truncation=True,
                                  is_pretokenized=True,
                                  max_length=512)).unsqueeze(0)

        with torch.no_grad():
            outputs = self.model(input_ids)

        predictions = torch_fun.softmax(outputs[0].squeeze(), dim=-1)
        max_predictions = torch.argmax(predictions, dim=-1)

        predicted_labels = [
            (idx, label_idx)
            for idx, label_idx in enumerate(max_predictions)
            if self.labels_map[label_idx.item()] not in _IGNORE_LABELS
        ]

        final_labels = []
        for idx, label_idx in predicted_labels:
            word = self.tokenizer.convert_ids_to_tokens(
                int(input_ids.squeeze()[idx]))
            entity_label = self.labels_map[label_idx.item()]

            if not word.startswith('##') and word not in _SPECIAL_TOKENS:
                final_labels.append(entity_label)

        return final_labels

    # TODO: Take advantage of sentence batching in tokenizer
    def predict(self, sentences):
        """Predict the named entity labels of a list of sentences.

        Args:
            sentences (:obj:`list` of :obj:`list` of :obj:`str`): The input
                sentences.

        Returns:
            :obj:`list` of :obj:`list` of :obj:`str`: The predicted
            named entity labels for the given sentences.
        """

        sentences_entities = []
        for idx, sentence in enumerate(sentences):
            sentences_entities.append(self.predict_sentence(sentence))

        return sentences_entities
