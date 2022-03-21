
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


"""This module contains the CAMeL Tools sentiment analyzer component.
"""

import torch
import torch.nn.functional as torch_fun
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification

from camel_tools.data import CATALOGUE


_LABELS = ('positive', 'negative', 'neutral')


class SentimentDataset(Dataset):
    """Sentiment PyTorch Dataset

    Args:
        sentences (:obj:`list` of :obj:`list` of :obj:`str`): The input
            sentences.
        tokenizer (:obj:`PreTrainedTokenizer`): Bert's pretrained tokenizer.
        max_seq_length (:obj:`int`):  Maximum sentence length.
    """

    def __init__(self, sentences, tokenizer, max_seq_length):
        self.encoded_sents = tokenizer(sentences, add_special_tokens=True,
                                       padding=True, max_length=max_seq_length,
                                       truncation=True, return_tensors="pt")

    def __getitem__(self, idx):
        return {
            'input_ids': self.encoded_sents.input_ids[idx],
            'token_type_ids':  self.encoded_sents.token_type_ids[idx],
            'attention_mask': self.encoded_sents.attention_mask[idx]
        }

    def __len__(self):
        return self.encoded_sents.input_ids.shape[0]


class SentimentAnalyzer:
    """CAMeL Tools sentiment analysis component.

    Args:
        model_path (:obj:`str`): The path to the fine-tuned model.
        use_gpu (:obj:`bool`, optional): The flag to use a GPU or not.
            Defaults to True.
    """

    def __init__(self, model_path, use_gpu=True):
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.labels_map = self.model.config.id2label
        self.use_gpu = use_gpu

    @staticmethod
    def pretrained(model_name=None, use_gpu=True):
        """Load a pre-trained model provided with camel_tools.

        Args:
            model_name (:obj:`str`, optional): Name of pre-trained model to
                load.
                Two models are available: 'arabert' and 'mbert'.
                If None, the default model ('arabert') will be loaded.
                Defaults to None.
            use_gpu (:obj:`bool`, optional): The flag to use a GPU or not.
                Defaults to True.

        Returns:
            :obj:`SentimentAnalyzer`: Instance with loaded pre-trained model.
        """

        if model_name is None:
            model_name = CATALOGUE.components['SentimentAnalysis'].default

        model_info = (CATALOGUE.components['SentimentAnalysis']
                      .datasets[model_name])
        model_path = str(model_info.path)

        return SentimentAnalyzer(model_path, use_gpu)

    @staticmethod
    def labels():
        """Get the list of possible sentiment labels returned by predictions.

        Returns:
            :obj:`list` of :obj:`str`: List of sentiment labels.
        """

        return list(_LABELS)

    def predict_sentence(self, sentence):
        """Predict the sentiment label of a single sentence.

        Args:
            sentence (:obj:`str`): Input sentence.

        Returns:
            :obj:`str`: The predicted sentiment label for given sentence.
        """

        return self.predict([sentence])[0]

    def predict(self, sentences, batch_size=32):
        """Predict the sentiment labels of a list of sentences.

        Args:
            sentences (:obj:`list` of :obj:`str`): Input sentences.
            batch_size (:obj:`int`): The batch size.

        Returns:
            :obj:`list` of :obj:`str`: The predicted sentiment labels for given
            sentences.
        """

        sentiment_dataset = SentimentDataset(sentences, self.tokenizer,
                                             max_seq_length=512)

        data_loader = DataLoader(sentiment_dataset, batch_size=batch_size,
                                 shuffle=False, drop_last=False)

        device = ('cuda' if self.use_gpu and torch.cuda.is_available() else
                  'cpu')

        self.model.to(device)
        self.model.eval()

        with torch.no_grad():
            for batch in data_loader:
                batch = {k: v.to(device) for k, v in batch.items()}
                inputs = {'input_ids': batch['input_ids'],
                          'token_type_ids': batch['token_type_ids'],
                          'attention_mask': batch['attention_mask']}
                logits = self.model(**inputs)[0]

        predictions = torch_fun.softmax(logits, dim=-1)
        max_predictions = torch.argmax(predictions, dim=-1)
        predicted_labels = [self.labels_map[p.item()] for p in max_predictions]

        return predicted_labels
