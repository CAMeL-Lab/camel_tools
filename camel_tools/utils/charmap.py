# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2019 New York University Abu Dhabi
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

"""Contains the CharMapper class (for mapping characters in a Unicode string to
other strings) and custom exceptions raised by CharMapper.
"""

from __future__ import absolute_import

from collections import deque, Mapping
import os
import json


from builtins import range  # pylint: disable=W0622
import six

from .stringutils import isunicode


class InvalidCharMapKeyError(ValueError):
    """Exception raised when an invalid key is found in a charmap used to
    initialize :obj:`CharMapper`.
    """

    def __init__(self, key, message):
        super(InvalidCharMapKeyError, self).__init__(message)
        self.key = key
        self.message = message

    def __repr__(self):
        return 'InvalidCharMapKeyError({}, {})'.format(
            repr(self.key), repr(self.message)
        )

    def __str__(self):
        return self.message


class BuiltinCharMapNotFoundError(ValueError):
    """Exception raised when a specified map name passed to
    :func:`CharMapper.builtin_mapper` is not in the list of builtin maps.
    """

    def __init__(self, map_name, message):
        super(BuiltinCharMapNotFoundError, self).__init__(message)
        self.map_name = map_name
        self.message = message

    def __repr__(self):
        return 'BuiltinCharMapNotFoundError({}, {})'.format(
            repr(self.map_name), repr(self.message)
        )

    def __str__(self):
        return self.message


class CharMapper(object):
    """A class for mapping characters in a Unicode string to other strings.

    Args:
        charmap (:obj:`dict`): A dictionary or any other dictionary-like
            obeject (implementing collections.Mapping) mapping characters
            or range of characters to a string. Keys in the dictionary
            should be Unicode strings of length 1 or 3. Strings of length 1
            indicate a single character to be mapped, while strings of
            length 3 indicate a range. Range strings should have the format
            'a-b' where is the starting character in the range and 'b' is
            the last character in the range (inclusive). 'b' should have a
            strictly larger ordinal number than 'a'. Dictionary values
            should be either strings or `None`, where `None` indicates that
            characters are mapped to themselves. Use an empty string to
            indicate deletion.
        default (:obj:`str`, optional): The default value to map characters
            not in **charmap** to. `None` indicates that characters map to
            themselves. Defaults to `None`.

    Raises:
        :obj:`InvalidCharMapKeyError`: If a key in charmap is not a Unicode
            string containing either a single character or a valid
            character range.
        :obj:`TypeError`: If default or a value for a key in charmap is
            neither `None` nor a Unicode string, or if **charmap** is not a
            dictionary-like object.
    """

    BUILTIN_CHARMAPS = frozenset((
        'ar2bw',
        'ar2safebw',
        'ar2xmlbw',
        'ar2hsb',
        'bw2ar',
        'bw2safebw',
        'bw2xmlbw',
        'bw2hsb',
        'safebw2ar',
        'safebw2bw',
        'safebw2xmlbw',
        'safebw2hsb',
        'xmlbw2ar',
        'xmlbw2bw',
        'xmlbw2safebw',
        'xmlbw2hsb',
        'hsb2ar',
        'hsb2bw',
        'hsb2safebw',
        'hsb2xmlbw',
        'arclean',
    ))

    @staticmethod
    def _expand_char_map(charmap):
        """Creates a new dictionary from charmap where character ranges are
        expanded and given their own dictionary entry.

        Args:
            charmap (:obj:`dict`): The character map to be expanded.

        Raises:
            :obj:`InvalidCharMapKeyError`: If a key in **charmap** is not a
                Unicode string containing either a single character or a valid
                character range.
            :obj:`TypeError`: If a value for a key in **charmap** is neither
                `None` nor a Unicode string.
        """

        # TODO: Implement a space efficient character map data structure

        new_map = {}

        for key in charmap.keys():
            # Check that key is a string
            if not isunicode(key):
                raise TypeError('Expected string as key. '
                                'Got {} instead.'.format(type(key)))

            # If string is one character long we can directly add it to the map
            if len(key) == 1:
                if charmap[key] is not None and not isunicode(charmap[key]):
                    raise TypeError(
                        ('Expected a Unicode string or None value for key '
                         'value, got {} instead.').format(type(charmap[key])))
                else:
                    new_map[key] = charmap[key]

            # We check if it's a range with the following rules:
            #     a) The string is 3 character long with a dash '-' in the
            #        middle.
            #     b) The first character must have a strictly smaller ordinal
            #        than the last character.
            elif len(key) == 3 and key[1] == '-':
                if ord(key[0]) >= ord(key[2]):
                    raise InvalidCharMapKeyError(key, '')
                else:
                    if (charmap[key] is not None
                            and not isunicode(charmap[key])):
                        raise TypeError(
                            ('Expected a Unicode string or None value for key '
                             'value, got {} instead.').format(
                                 type(charmap[key]))
                        )
                    for char in range(ord(key[0]), ord(key[2]) + 1):
                        new_map[six.unichr(char)] = charmap[key]

            # Otherwise, we have an invalid map key
            else:
                raise InvalidCharMapKeyError(
                    key, 'Invalid character or character range')

        return new_map

    def __init__(self, charmap, default=None):
        """Class constructor.
        """

        if isinstance(charmap, Mapping):
            self._charmap = self._expand_char_map(charmap)
        else:
            raise TypeError(
                ('Expected a dictionary like object for charmap, got {} '
                 'instead').format(type(charmap)))

        if default is None or isunicode(default):
            self._default = default
        else:
            raise TypeError(
                ('Expected a Unicode string or None value for default, got {} '
                 'instead.').format(type(default)))

    def __call__(self, s):
        """Alias for :func:`CharMapper.map_string`.
        """
        return self.map_string(s)

    @staticmethod
    def mapper_from_json(fpath):
        """Creates a :obj:`CharMapper` instance from a JSON file.

        Args:
            fpath (:obj:`str`): Path to JSON file.

        Returns:
            :obj:`CharMapper`: A new :obj:`CharMapper` instance generated from
            given JSON file.

        Raises:
            :obj:`InvalidCharMapKeyError`: If a key in charmap is not a Unicode
                string containing either a single character or a valid
                character range.
            :obj:`TypeError`: If default or a value for a key in charmap is
                neither `None` nor a Unicode string.
            :obj:`FileNotFoundError`: If file at `fpath` doesn't exist.
            :obj:`JSONDecodeError`: If `fpath` is not a valid JSON file.
        """

        with open(fpath, 'r') as infile:
            jsonstr = infile.read()

            # With Python 2, we need to force the JSON string to Unicode
            if six.PY2:  # pragma: no coverage
                jsonstr = unicode(jsonstr)  # pylint: disable=E0602

            json_dict = json.loads(jsonstr)

        return CharMapper(
            json_dict.get('charMap', {}),
            default=json_dict.get('default', None)
        )

    @staticmethod
    def builtin_mapper(map_name):
        """Creates a :obj:`CharMapper` instance from built-in mappings.

        Args:
            map_name (:obj:`str`): Name of built-in map.

        Returns:
            :obj:`CharMapper`: A new :obj:`CharMapper` instance of built-in
            map.

        Raises:
            :obj:`BuiltinCharMapNotFound`: If `map_name` is not in the list of
                built-in maps.
        """

        if map_name not in CharMapper.BUILTIN_CHARMAPS:
            raise BuiltinCharMapNotFoundError(
                map_name,
                'No built in mapping with name \'{}\' '
                'was found.'.format(map_name))

        try:
            charmaps_dir = os.path.join(os.path.dirname(__file__), 'charmaps')

        # This should never happen unless there something wrong with the
        # system or the installation.
        except Exception:  # pragma: no coverage
            raise BuiltinCharMapNotFoundError(
                map_name,
                'Could not create mapping with name \'{}\'.'.format(map_name))

        map_path = os.path.join(charmaps_dir, '{}_map.json'.format(map_name))

        return CharMapper.mapper_from_json(map_path)

    def map_string(self, s):
        """Maps each character in a given string to its corresponding value in
        the charmap.

        Args:
            s (:obj:`str`): A Unicode string to be mapped.

        Returns:
            :obj:`str`: A new Unicode string with the charmap applied.

        Raises:
            :obj:`TypeError`: If s is not a Unicode string.
        """

        if not isunicode(s):
            raise TypeError((
                'Expected Unicode string as input, got {} instead.'
            ).format(type(s)))

        buff = deque()

        for char in s:
            transliteration = self._charmap.get(char, self._default)
            if transliteration is None:
                buff.append(char)
            else:
                buff.append(transliteration)

        return u''.join(buff)
