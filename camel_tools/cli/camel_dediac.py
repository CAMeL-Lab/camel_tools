#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2022 New York University Abu Dhabi
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

"""The CAMeL Tools de-diacritization utility.

Usage:
    camel_dediac [-s <SCHEME> | --scheme=<SCHEME>]
                 [-m <MARKER> | --marker=<MARKER>]
                 [-I | --ignore-markers]
                 [-S | --strip-markers]
                 [-o OUTPUT | --output=OUTPUT] [FILE]
    camel_dediac (-l | --list)
    camel_dediac (-v | --version)
    camel_dediac (-h | --help)

Options:
  -s <SCHEME> --scheme=<SCHEME>
        The encoding scheme of the input text. [default: ar]
  -o OUTPUT --output=OUTPUT
        Output file. If not specified, output will be printed to stdout.
  -m <MARKER> --marker=<MARKER>
        Marker used to prefix tokens not to be de-diacritized.
        [default: @@IGNORE@@]
  -I --ignore-markers
        De-diacritize words prefixed with a marker.
  -S --strip-markers
        Remove prefix markers in output if --ignore-markers is set.
  -l --list
        Show a list of available input encoding schemes.
  -h --help
        Show this screen.
  -v --version
        Show version.
"""


import re
import sys

from docopt import docopt

import camel_tools as camelt
from camel_tools.utils.dediac import dediac_ar, dediac_bw, dediac_safebw
from camel_tools.utils.dediac import dediac_xmlbw, dediac_hsb
from camel_tools.cli.utils import open_files


__version__ = camelt.__version__

_BUILTIN_SCHEMES = [
    ('ar', 'Arabic script', dediac_ar),
    ('bw', 'Buckwalter encoding', dediac_bw),
    ('safebw', 'Safe Buckwalter encoding', dediac_safebw),
    ('xmlbw', 'XML Buckwalter encoding', dediac_xmlbw),
    ('hsb', 'Habash-Soudi-Buckwalter encoding', dediac_hsb)
]

_WHITESPACE_RE = re.compile(r'\s+|\S+')


def _dediac_marked_tokens(tokens, dediac_fn, marker=None, strip_markers=False):
    result = []
    n = len(marker)

    if strip_markers:
        for token in tokens:
            if token.startswith(marker):
                    result.append(token[n:])
            else:
                result.append(dediac_fn(token))
    else:
        for token in tokens:
            if token.startswith(marker):
                    result.append(token)
            else:
                result.append(dediac_fn(token))

    return result


def main():  # pragma: no cover
    try:
        version = ('CAMeL Tools v{}'.format(__version__))
        arguments = docopt(__doc__, version=version)

        if arguments['--list']:
            for scheme in _BUILTIN_SCHEMES:
                print("{}   {}".format(scheme[0].ljust(8), scheme[1]))
            sys.exit(0)

        dediac_fn = None

        for scheme in _BUILTIN_SCHEMES:
            if scheme[0] == arguments['--scheme']:
                dediac_fn = scheme[2]

        if dediac_fn is None:
            sys.stderr.write('Error: {} is not a valid scheme.\n'
                                'Run `camel_dediac -l` to see the list'
                                ' of available schemes.'
                                '\n'.format(repr(arguments['--scheme'])))
            sys.exit(1)

        strip_markers = arguments['--strip-markers']
        marker = arguments['--marker']
        ignore_markers = arguments['--ignore-markers']

        # Open files (or just use stdin and stdout)
        fin, fout = open_files(arguments['FILE'], arguments['--output'])

        # De-diacritize lines
        try:
            if ignore_markers:
                for line in fin:
                    toks = _WHITESPACE_RE.findall(line)
                    dediac_toks = _dediac_marked_tokens(toks, dediac_fn,
                                                        marker, strip_markers)
                    fout.write(''.join(dediac_toks))
            else:
                for line in fin:
                    fout.write(dediac_fn(line))

        # If everything worked so far, this shouldn't happen
        except Exception:  # pylint: disable=W0703
            sys.stderr.write('Error: An unkown error occured during '
                                'de-diacritization.\n')
            sys.exit(1)

        # Cleanup
        if arguments['FILE'] is not None:
            fin.close()
        if arguments['--output'] is not None:
            fout.close()

        sys.exit(0)

    except KeyboardInterrupt:
        sys.stderr.write('Exiting...\n')
        sys.exit(1)

    except Exception:
        sys.stderr.write('Error: An unknown error occurred.\n')
        sys.exit(1)


if __name__ == '__main__':  # pragma: no cover
    main()
