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

"""Contains the Transliterator class (for transliterating text using a
CharMapper).
"""

from __future__ import absolute_import

from collections import deque
import re
import six

from camel_tools.utils.charmap import CharMapper


_WHITESPACE_RE = re.compile(r'\s')


class Transliterator(object):
    """A class for transliterating text using a CharMapper. This class adds the
    extra utility of marking individual tokens to not be transliterated. It
    assumes that tokens are whitespace seperated.
    """

    def __init__(self, mapper, marker='@@IGNORE@@'):
        """Initializes Transliterator with a CharMapper instance to be used for
        transliteration and a marker to mark tokens not to be transliterated.

         Args:
            mapper (CharMapper): The CharMapper instance to be used for
                transliteration.
            marker (str): A string that is prefixed to all tokens that
                shouldn't be ransliterated. The default value is '@@IGNORE@@'.
                Should not contain any whitespace characters.

        Raises:
            TypeError: If mapper is not a CharMapper instance or marker is not
                a string.
            ValueError: If marker contains whitespace or is an empty string.
        """

        self._mapper = mapper

        if not isinstance(mapper, CharMapper):
            raise TypeError('Mapper is not a CharMapper instance.')

        if not isinstance(marker, six.string_types):
            raise TypeError('Marker is not a string.')

        if not marker:
            raise ValueError('Marker is empty.')
        elif _WHITESPACE_RE.search(marker) is None:
            self._marker = marker
        else:
            raise ValueError('Marker contains whitespace.')

        self._markerre = re.compile(
            r'({}\S+)'.format(re.escape(marker)),
            re.UNICODE | re.MULTILINE
        )

    def transliterate(self, _string, strip_markers=False, ignore_markers=False):
        """Transliterate a given string.

        Args:
            _string (str): The string to transliterate.
            strip_markers (bool): Output is stripped of markers if True,
                otherwise markers are kept in the output. Set to False by
                default.
            ignore_markers (bool): If set to True, all text, including marked
                tokens are transliterated as well excluding the markers. Set to
                False by default. If you would like to transliterate the
                markers as well, use the CharMapper directly instead.

        Returns:
            str: The transliteration of _string with the exception of marked
                words.
        """

        buff = deque()

        splits = self._markerre.split(_string)
        for spl in splits:
            if spl.startswith(self._marker):
                if ignore_markers:
                    if not strip_markers:
                        buff.append(self._marker)
                    buff.append(
                        self._mapper.map_string(spl[len(self._marker):])
                    )
                else:
                    if strip_markers:
                        buff.append(spl[len(self._marker):])
                    else:
                        buff.append(spl)
            else:
                buff.append(self._mapper.map_string(spl))

        return u''.join(buff)
