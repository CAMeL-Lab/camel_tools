# -*- coding: utf-8 -*-

from __future__ import absolute_import

from collections import deque, Mapping

import six
from builtins import range

from .stringutils import isUnicode


class InvalidCharMapKeyError(Exception):

    def __init__(self, key, message):
        self.key = key
        self.message = message


class CharMapper(object):
    """A class for mapping characters in a unicode string to other strings.
    """

    @staticmethod
    def _expandCharMap(charMap):
        """Creates a new dictionary from charMap where character ranges are
        expanded and given their own dictionary entry.

        Args:
            charMap (dict): The character map to be expanded.

        Raises:
            InvalidCharMapKeyError: If a key in charMap is not a unicode string
                containing either a single character or a valid character
                range.
            TypeError: If a value for a key in charMap is neither None nor a
                unicode string.
        """

        # TODO: Implement a space efficient character map data structure

        newMap = {}

        for k in charMap.keys():
            # Check that key is a string
            if not isUnicode(k):
                raise(TypeError('Expected string as key. '
                                'Got {} instead.'.format(type(k))))

            # If string is one character long we can directly add it to the map
            if len(k) == 1:
                if charMap[k] is not None and not isUnicode(charMap[k]):
                    raise(TypeError(
                        ('Expected a unicode string or None value for key '
                         'value, got {} instead.').format(type(charMap[k]))
                    ))
                else:
                    newMap[k] = charMap[k]

            # We check if it's a range with the following rules:
            #     a) The string is 3 character long with a dash '-' in the
            #        middle.
            #     b) The first character must have a strictly smaller ordinal
            #        than the last character.
            elif len(k) == 3 and k[1] == '-':
                if ord(k[0]) >= ord(k[2]):
                    raise(InvalidCharMapKeyError(k, ''))
                else:
                    if charMap[k] is not None and not isUnicode(charMap[k]):
                        raise(TypeError(
                            ('Expected a unicode string or None value for key '
                             'value, got {} instead.').format(type(charMap[k]))
                        ))
                    for c in range(ord(k[0]), ord(k[2]) + 1):
                        newMap[six.unichr(c)] = charMap[k]

            # Otherwise, we have an invalid map key
            else:
                raise(InvalidCharMapKeyError(
                    k, 'Invalid character or character range'))

        return newMap

    def __init__(self, charMap, default=None):
        """Initializes CharMapper with a give character map and a default
        value for unmapped characters.

        Args:
            charMap (dict): A dictionary or any other dictionary-lik obeject
                (implementing collections.Mapping) mapping characters or range
                of characters to a string. Keys in the dictionary should be
                unicode strings of length 1 or 3. Strings of length 1 indicate
                a single character to be mapped, while strings of length 3
                indicate a range. Range strings should have the format 'a-b'
                where is the starting character in the range and 'b' is the
                last character in the range (inclusive). 'b' should have a
                strictly larger ordinal number than 'a'. Dictionary values
                should be either strings or None, where None indicates that
                characters are mapped to themselves. Use an empty string to
                indicate deletion.
            default (:obj:`str`, optional): The default value to map characters
                not in charMap to. None indicates that characters map to
                themselves. Set to None by default.

        Raises:
            InvalidCharMapKeyError: If a key in charMap is not a unicode string
                containing either a single character or a valid character
                range.
            TypeError: If default or a value for a key in charMap is neither
                None nor a unicode string, or if charMap is not a
                dictionary-like object.
        """

        if isinstance(charMap, Mapping):
            self._charMap = self._expandCharMap(charMap)
        else:
            raise(TypeError(
                ('Expected a dictionary like object for charMap, got {} '
                 'instead').format(type(charMap))))

        if default is None or isUnicode(default):
            self._default = default
        else:
            raise TypeError(
                ('Expected a unicode string or None value for default, got {} '
                 'instead.').format(type(default)))

    def mapString(self, s):
        """Maps each character in a given string to its corresponding value in
        the charMap.

        Args:
            s (str): A unicode string to be mapped.

        Returns:
            A new unicode string with the charMap applied.

        Raises:
            TypeError: If s is not a unicode string.
        """

        if not isUnicode(s):
            raise(TypeError((
                'Expected unicode string as input, got {} instead.'
            ).format(type(s))))

        buff = deque()

        for c in s:
            cNew = self._charMap.get(c, self._default)
            if cNew is None:
                buff.append(c)
            else:
                buff.append(cNew)

        return u''.join(buff)
