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
