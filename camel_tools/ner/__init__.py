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


"""This module contains the CAMeL Tools NER component.
"""


import torch
import torch.nn.functional as torch_fun
from transformers import BertTokenizer, BertForTokenClassification

from camel_tools.data import get_dataset_path


_DEFAULT_DATA_PATH = get_dataset_path('NamedEntityRecognition')
_LABELS = ['B-LOC', 'B-ORG', 'B-PERS', 'I-LOC', 'I-ORG', 'I-PERS']
_IGNORE_LABELS = ['O']
_SPECIAL_TOKENS = ['[SEP]', '[CLS]']


class NERecognizer:
    """CAMeL Tools NER component.

    Args:
        model_path(:obj:`str`): The path to the fine-tuned model.
    """

    def __init__(self, model_path):
        self.model = BertForTokenClassification.from_pretrained(model_path)
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
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

        model_path = str(get_dataset_path('NamedEntityRecognition', model_name))
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
            sentence (:obj:`list` of :obj:`str`): Input sentence.

        Returns:
            :obj:`list` of :obj:`dict`: The predicted named entity
            labels for a given sentence.
        """

        # Add special tokens takes care of adding [CLS], [SEP] tokens
        input_ids = torch.tensor(
            self.tokenizer.encode(sentence, add_special_tokens=True,
                                  truncation=True,
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

        entities = []
        for idx, label_idx in predicted_labels:
            word = self.tokenizer.convert_ids_to_tokens(
                int(input_ids.squeeze()[idx]))
            entity_label = self.labels_map[label_idx.item()]

            entity = {
                "word": word,
                "entity": entity_label,
                "idx": idx - 1
            }

            if word not in _SPECIAL_TOKENS:
                entities.append(entity)

        return entities

    def predict(self, sentences):
        """Predict the named entity labels of a list of sentences.

        Args:
            sentences (:obj:`list` of :obj:`list` of :obj:`str`): The input
                sentences.

        Returns:
            :obj:`list` of :obj:`list` of :obj:`dict`: The predicted
            named entity labels for given sentences.
        """

        sentences_entities = []
        for idx, sentence in enumerate(sentences):
            sentences_entities.append(self.predict_sentence(sentence))

        return sentences_entities
