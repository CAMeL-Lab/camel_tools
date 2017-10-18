# -*- coding: utf-8 -*-

from __future__ import absolute_import

from collections import deque, Mapping
import os
import json

import six
from builtins import range

from .stringutils import isUnicode


class InvalidCharMapKeyError(Exception):

    def __init__(self, key, message):
        self.key = key
        self.message = message


class BuiltinCharMapNotFound(Exception):

    def __init__(self, mapName, message):
        self.mapName = mapName
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

    @staticmethod
    def mapperFromJson(fpath):
        """Creates a CharMapper instance from a json file.

        Json files should have the following format:

            {
                "default": ...,

                "charMap": {
                    ...
                }
            }

        "default" and "charMap" follow the same rules as described in
        CharMapper.__init__ with json keyword 'null' used instead of None.

        If "default" is not specified, it will default to None.
        If "charMap" is not specified, it will default to an empty dictionary.

        Args:
            fpath (str): Path to json file.

        Returns:
            CharMapper: A new CharMapper instance generated from given json
                file.

        Raises:
            InvalidCharMapKeyError: If a key in charMap is not a unicode string
                containing either a single character or a valid character
                range.
            TypeError: If default or a value for a key in charMap is neither
                None nor a unicode string, or if charMap is not a
                dictionary-like object.
            FileNotFoundError: If file at fpath doesn't exist.
            JSONDecodeError: If fpath is not a valid JSON file.
        """

        with open(fpath, 'r') as infile:
            jsonstr = infile.read()

            # With Python 2, we need to force the JSOn string to unicode
            if six.PY2:  # pragma: no coverage
                jsonstr = unicode(jsonstr)

            jsonDict = json.loads(jsonstr)

        return CharMapper(
            jsonDict.get('charMap', {}),
            default=jsonDict.get('default', None))

    @staticmethod
    def builtinMapper(mapName):
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
            mapName (str): Name of built-in map.

        Returns:
            CharMapper: A new CharMapper instance of built-in map.

        Raises:
            InvalidCharMapKeyError: If a key in charMap is not a unicode string
                containing either a single character or a valid character
                range.
            TypeError: If default or a value for a key in charMap is neither
                None nor a unicode string, or if charMap is not a
                dictionary-like object.
            JSONDecodeError: If fpath is not a valid JSON file.
            BuiltinCharMapNotFound: If mapName is not in the list of built-in
                maps.
        """

        if mapName not in [
            'ar2bw',
            'ar2safebw',
            'ar2xmlbw',
            'ar2hsb',
            'bw2ar',
            'safebw2ar',
            'xmlbw2ar',
            'hsb2ar',
            'arclean'
        ]:
            raise(BuiltinCharMapNotFound(
                mapName,
                'No built in mapping with name \'{}\' '
                'was found.'.format(mapName)))

        try:
            charMapsDir = os.path.join(os.path.dirname(__file__), 'charmaps')

        # This should never happen unless there something wrong with the
        # system or the installation.
        except Exception:  # pragma: no coverage
            raise(BuiltinCharMapNotFound(
                mapName,
                'Could not create mapping with name \'{}\'.'.format(mapName)))

        mapPath = os.path.join(charMapsDir, '{}_map.json'.format(mapName))

        return CharMapper.mapperFromJson(mapPath)

    def mapString(self, s):
        """Maps each character in a given string to its corresponding value in
        the charMap.

        Args:
            s (str): A unicode string to be mapped.

        Returns:
            str: A new unicode string with the charMap applied.

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
