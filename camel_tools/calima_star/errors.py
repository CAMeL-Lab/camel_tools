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

"""CALIMA Star error classes.
"""


class CalimaStarError(Exception):
    """Base class for all CALIMA Star errors.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


# Database Errors

class DatabaseError(CalimaStarError):
    """Base class for errors thrown by Database component.
    """

    def __init__(self, msg):
        CalimaStarError.__init__(self, msg)


class InvalidBuiltinDatabaseName(DatabaseError):
    """Error thrown when an invalid builtin database name is given.
    """

    def __init__(self, dbname):
        DatabaseError.__init__(self,
                               'Invalid builtin database with name {}'.format(
                                repr(dbname)))


class InvalidDatabaseFlagError(DatabaseError):
    """Error thrown while parsing a database file.
    """

    def __init__(self, flag):
        DatabaseError.__init__(self, 'Invalid flag value {}'.format(
            repr(flag)))


class DatabaseParseError(DatabaseError):
    """Error thrown while parsing a database file.
    """

    def __init__(self, msg):
        DatabaseError.__init__(self, 'Error parsing database ({})'.format(msg))


# Analyzer Errors

class AnalyzerError(CalimaStarError):
    """Class for errors thrown by Analyzer component.
    """

    def __init__(self, msg):
        CalimaStarError.__init__(self, msg)


# Generator Errors

class GeneratorError(CalimaStarError):
    """Base class for errors thrown by Generator component.
    """

    def __init__(self, msg):
        CalimaStarError.__init__(self, msg)


class InvalidGeneratorFeature(GeneratorError):
    """Error thrown when an invalid feature
    """

    def __init__(self, feat):
        GeneratorError.__init__(self, 'Invalid feature {}'.format(repr(feat)))


class InvalidGeneratorFeatureValue(GeneratorError):
    """Error thrown when an invalid value is given to a feature.
    """

    def __init__(self, feat, val):
        GeneratorError.__init__(self, 'Invalid value {} for feature {}'.format(
            repr(val), repr(feat)))


# Reinflector Errors

class ReinflectorError(CalimaStarError):
    """Base class for errors thrown by Reinflector component.
    """

    def __init__(self, msg):
        CalimaStarError.__init__(self, msg)


class InvalidReinflectorFeature(ReinflectorError):
    """Error thrown when an invalid feature
    """

    def __init__(self, feat):
        GeneratorError.__init__(self, 'Invalid feature {}'.format(repr(feat)))


class InvalidReinflectorFeatureValue(ReinflectorError):
    """Error thrown when an invalid value is given to a feature.
    """

    def __init__(self, feat, val):
        GeneratorError.__init__(self, 'Invalid value {} for feature {}'.format(
            repr(val), repr(feat)))
