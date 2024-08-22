# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2024 New York University Abu Dhabi
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
This Dialect Identification system can identify between 25 Arabic city dialects
as well as Modern Standard Arabic. It is based on the system described by
`Salameh, Bouamor and Habash <http://www.aclweb.org/anthology/C18-1113>`_.
"""


import collections


__all__ = [
    'DIDPred',
    'DialectIdError',
    'UntrainedModelError',
    'InvalidDataSetError',
    'PretrainedModelError',
]


class DIDPred(collections.namedtuple('DIDPred', ['top', 'scores'])):
    """A named tuple containing dialect ID prediction results.

    Attributes:
        top (:obj:`str`): The dialect label with the highest score. See
            :ref:`dialectid_labels` for a list of output labels.
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
        msg = ('Invalid data set name {}. Valid names are "DEV" and '
               '"TEST"'.format(repr(dataset)))
        DialectIdError.__init__(self, msg)


class PretrainedModelError(DialectIdError):
    """Error thrown when attempting to load a pretrained model provided with
    camel-tools.
    """

    def __init__(self, msg):
        DialectIdError.__init__(self, msg)
