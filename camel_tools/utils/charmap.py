# -*- coding: utf-8 -*-

"""Contains the CharMapper class (for mapping characters in a unicode string to
other strings) and custom exceptions raised by CharMapper.
"""

from __future__ import absolute_import

from collections import deque, Mapping
import os
import json


from builtins import range  #pylint: disable=W0622
import six

from .stringutils import isunicode


class InvalidCharMapKeyError(ValueError):
    """Exception raised when an invalid key is found in a charmap used to
    initialize CharMapper.
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
    CharMapper.builtin_mapper is not in the list of builtin maps.
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
    """A class for mapping characters in a unicode string to other strings.
    """

    BUILTIN_CHARMAPS = (
        'ar2bw',
        'ar2safebw',
        'ar2xmlbw',
        'ar2hsb',
        'bw2ar',
        'safebw2ar',
        'xmlbw2ar',
        'hsb2ar',
        'arclean',
    )

    @staticmethod
    def _expand_char_map(charmap):
        """Creates a new dictionary from charmap where character ranges are
        expanded and given their own dictionary entry.

        Args:
            charmap (dict): The character map to be expanded.

        Raises:
            InvalidCharMapKeyError: If a key in charmap is not a unicode string
                containing either a single character or a valid character
                range.
            TypeError: If a value for a key in charmap is neither None nor a
                unicode string.
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
                        ('Expected a unicode string or None value for key '
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
                            ('Expected a unicode string or None value for key '
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
        """Initializes CharMapper with a give character map and a default
        value for unmapped characters.

        Args:
            charmap (dict): A dictionary or any other dictionary-lik obeject
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
                not in charmap to. None indicates that characters map to
                themselves. Set to None by default.

        Raises:
            InvalidCharMapKeyError: If a key in charmap is not a unicode string
                containing either a single character or a valid character
                range.
            TypeError: If default or a value for a key in charmap is neither
                None nor a unicode string, or if charmap is not a
                dictionary-like object.
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
                ('Expected a unicode string or None value for default, got {} '
                 'instead.').format(type(default)))

    @staticmethod
    def mapper_from_json(fpath):
        """Creates a CharMapper instance from a json file.

        Json files should have the following format:

            {
                "default": ...,

                "charmap": {
                    ...
                }
            }

        "default" and "charmap" follow the same rules as described in
        CharMapper.__init__ with json keyword 'null' used instead of None.

        If "default" is not specified, it will default to None.
        If "charmap" is not specified, it will default to an empty dictionary.

        Args:
            fpath (str): Path to json file.

        Returns:
            CharMapper: A new CharMapper instance generated from given json
                file.

        Raises:
            InvalidCharMapKeyError: If a key in charmap is not a unicode string
                containing either a single character or a valid character
                range.
            TypeError: If default or a value for a key in charmap is neither
                None nor a unicode string, or if charmap is not a
                dictionary-like object.
            FileNotFoundError: If file at fpath doesn't exist.
            JSONDecodeError: If fpath is not a valid JSON file.
        """

        with open(fpath, 'r') as infile:
            jsonstr = infile.read()

            # With Python 2, we need to force the JSOn string to unicode
            if six.PY2:  # pragma: no coverage
                jsonstr = unicode(jsonstr)  #pylint: disable=E0602

            json_dict = json.loads(jsonstr)

        return CharMapper(
            json_dict.get('charMap', {}),
            default=json_dict.get('default', None)
        )

    @staticmethod
    def builtin_mapper(map_name):
        """Creates a CharMapper instance from built-in mappings.

        List of built-in mappings:

            ----------------- Arabic Transliteration -----------------

                'ar2bw': Transliterates Arabic text to Buckwalter scheme.
            'ar2safebw': Transliterates Arabic text to Safe Buckwalter scheme.
             'ar2xmlbw': Transliterates Arabic text to XML Buckwalter scheme.
               'ar2hsb': Transliterates Arabic text to  Habash-Soudi-Buckwalter
                         scheme.
                'bw2ar': Transliterates Buckwalter scheme text to Arabic.
            'safebw2ar': Transliterates Safe Buckwalter scheme text to Arabic.
             'xmlbw2ar': Transliterates XML Buckwalter Scheme text to Arabic.
               'hsb2ar': Transliterates Habash-Soudi-Buckwalter scheme text to
                         Arabic.

            ------------------------ Utility ------------------------

              'arclean': Cleans Arabic text by:
                           - Deleting characters that are not in Arabic, ASCII,
                             or Latin-1.
                           - Converting all spacing characters to an ASCII
                             space character.
                           - Converting Indic digits into Arabic digits.
                           - Converting extended Arabic letters into basic
                             Arabic letters.
                           - Converting 1-char presentation froms into simple
                             basic forms.
                         .

        Args:
            map_name (str): Name of built-in map.

        Returns:
            CharMapper: A new CharMapper instance of built-in map.

        Raises:
            InvalidCharMapKeyError: If a key in charmap is not a unicode string
                containing either a single character or a valid character
                range.
            TypeError: If default or a value for a key in charmap is neither
                None nor a unicode string, or if charmap is not a
                dictionary-like object.
            JSONDecodeError: If fpath is not a valid JSON file.
            BuiltinCharMapNotFound: If map_name is not in the list of built-in
                maps.
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

    def map_string(self, _string):
        """Maps each character in a given string to its corresponding value in
        the charmap.

        Args:
            _string (str): A unicode string to be mapped.

        Returns:
            str: A new unicode string with the charmap applied.

        Raises:
            TypeError: If s is not a unicode string.
        """

        if not isunicode(_string):
            raise TypeError((
                'Expected unicode string as input, got {} instead.'
            ).format(type(_string)))

        buff = deque()

        for char in _string:
            transliteration = self._charmap.get(char, self._default)
            if transliteration is None:
                buff.append(char)
            else:
                buff.append(transliteration)

        return u''.join(buff)
