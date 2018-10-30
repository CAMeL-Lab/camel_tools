# -*- coding: utf-8 -*-

"""A collection of useful helper functions when working with strings.
"""


from __future__ import absolute_import

import six


def isunicode(obj):
    """Checks if an object is a unicode encoded string. Useful for Python 2 and
    3 compatibility.

    Args:
        obj (obj): The object to check.

    Returns:
        bool: True if obj is a unicode encoded string, False otherwise.
    """

    return isinstance(obj, six.text_type)


def force_unicode(s, encoding='utf-8'):
    """Convert a given string into a Unicode (decoded) string if it isn't
    already.

    Arguments:
        s {str} -- String object to convert.

    Keyword Arguments:
        encoding {str} -- The encoding of s if it is encoded
            (default: {'utf-8'}).

    Returns:
        {str} -- A Unicode (decoded) version of s.
    """

    if isinstance(s, six.text_type):
        return s
    else:
        return s.decode(encoding)


def force_encoding(s, encoding='utf-8'):
    """Convert a given string into an encoded string if it isn't already.

    Arguments:
        s {str} -- String object to convert.

    Keyword Arguments:
        encoding {str} -- The encoding s should be encoded into. Note that if s
            is already encoded, it is returned as is, even though it is in a
            differnet encoding than what is passed to this parameter.
            (default: {'utf-8'})

    Returns:
        {str} -- An encoded version of s.
    """

    if isinstance(s, six.binary_type):
        return s
    else:
        return s.encode(encoding)
