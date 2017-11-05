# -*- coding: utf-8 -*-

"""
A collection of useful helper functions when working with strings.
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

    if isinstance(obj, six.text_type):
        return True

    return False
