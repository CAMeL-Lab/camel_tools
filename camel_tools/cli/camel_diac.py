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


"""The CAMeL Tools diacritization utility.

Usage:
    camel_diac [-d DATABASE | --db=DATABASE]
               [-m MARKER | --marker=MARKER]
               [-I | --ignore-markers]
               [-S | --strip-markers]
               [-p | --pretokenized]
               [-o OUTPUT | --output=OUTPUT] [FILE]
    camel_diac (-l | --list-schemes)
    camel_diac (-v | --version)
    camel_diac (-h | --help)

Options:
  -d DATABASE --db=DATABASE
        Morphology database to use. DATABASE could be the name of a builtin
        database or a path to a database file. [default: calima-msa-r13]
  -o OUTPUT --output=OUTPUT
        Output file. If not specified, output will be printed to stdout.
  -m MARKER --marker=MARKER
        Marker used to prefix tokens not to be transliterated.
        [default: @@IGNORE@@]
  -I --ignore-markers
        Transliterate marked words as well.
  -S --strip-markers
        Remove markers in output.
  -p --pretokenized
        Input is already pre-tokenized by punctuation. When this is set,
        camel_diac will not split tokens by punctuation but any tokens that
        do contain punctuation will not be diacritized.
  -l --list
        Show a list of morphological databases.
  -h --help
        Show this screen.
  -v --version
        Show version.
"""


import re
import sys

from docopt import docopt

import camel_tools
from camel_tools.morphology.database import MorphologyDB
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.cli.utils import open_files


__version__ = camel_tools.__version__

_BUILTIN_DBS = MorphologyDB.list_builtin_dbs()
_DEFAULT_DB = 'calima-msa-r13'
_WHITESPACE_RE = re.compile(r'\s+|\S+')


def _diac_tokens(tokens, disambig, ignore_markers, marker, strip_markers,
                 pretokenized):
    result = []

    for token in tokens:
        if len(token.strip()) == 0:
            result.append(token)
        elif ignore_markers and token.startswith(marker):
            if strip_markers:
                result.append(token[len(marker):])
            else:
                result.append(token)
        else:
            if pretokenized:
                subtokens = [token]
            else:
                subtokens = simple_word_tokenize(token)
            disambig_tokens = disambig.disambiguate(subtokens)
            result.extend([d.analyses[0].analysis.get('diac', d.word)
                           for d in disambig_tokens])

    return result


def main():
    try:
        version = ('CAMeL Tools v{}'.format(__version__))
        arguments = docopt(__doc__, version=version)

        if arguments['--list']:
            for db_entry in _BUILTIN_DBS:
                print("{}   {}".format(db_entry.name.ljust(8),
                                       db_entry.description))
            sys.exit(0)

        db_name = None

        for db_entry in _BUILTIN_DBS:
            if arguments['--db'] == db_entry.name:
                db_name = db_entry.name

        if db_name is None:
            sys.stderr.write('Error: {} is not a valid database name.\n'
                             'Run `camel_diac -l` to see the list of available'
                             ' databases.\n'.format(repr(arguments['--db'])))
            sys.exit(1)

        disambig = MLEDisambiguator.pretrained(db_name)

        marker = arguments['--marker']
        ignore_markers = arguments['--ignore-markers']
        strip_markers = arguments['--strip-markers']
        pretokenized = arguments['--pretokenized']

        # Open files (or just use stdin and stdout)
        fin, fout = open_files(arguments['FILE'], arguments['--output'])

        # Diacritize lines
        try:
            for line in fin:
                toks = _WHITESPACE_RE.findall(line)
                diac_toks = _diac_tokens(toks, disambig, ignore_markers,
                                         marker, strip_markers, pretokenized)
                fout.write(''.join(diac_toks))

        # If everything worked so far, this shouldn't happen
        except Exception:  # pylint: disable=W0703
            sys.stderr.write('Error: An unkown error occured during '
                             'diacritization.\n')
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
