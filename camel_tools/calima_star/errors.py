# -*- coding: utf-8 -*-


"""CALIMA Star error classes.
"""


class CalimaStarError(Exception):
    """Base error class for all CALIMA Star errors.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


# Database Errors

class DatabaseError(CalimaStarError):
    """Class for errors thrown by Database component.
    """

    def __init__(self, msg):
        CalimaStarError.__init__(self, msg)


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
    """Class for errors thrown by Generator component.
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
    """Class for errors thrown by Reinflector component.
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
