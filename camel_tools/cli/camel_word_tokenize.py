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


"""The CAMeL Tools word tokenization utility.

This tool splits words from punctuation while collapsing contiguous segments of
spaces into a single whitespace character. It is also language agnostic and
splits all characters marked as punctuation or symbols in the Unicode
specification.

For example the following sentence:

> Hello,     world!!!!

becomes:

> Hello , world ! ! ! !

At the moment, this tool splits all punctuation indiscriminately.

Usage:
    camel_word_tokenize [-o OUTPUT | --output=OUTPUT] [FILE]
    camel_word_tokenize (-v | --version)
    camel_word_tokenize (-h | --help)

Options:
  -o OUTPUT --output=OUTPUT
        Output file. If not specified, output will be printed to stdout.
  -h --help
        Show this screen.
  -v --version
        Show version.
"""


import sys

from docopt import docopt

import camel_tools
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.cli.utils import open_files

from camel_tools.cli.utils import open_files


__version__ = camel_tools.__version__


_TOKENIZERS = [
    ('simple_word_tokenize', simple_word_tokenize)
]


def main():  # pragma: no cover
    try:
        version = ('CAMeL Tools v{}'.format(__version__))
        arguments = docopt(__doc__, version=version)

        # A bit redundant for now, but makes adding new tokenizers easier in
        # future
        tokenize_fn = simple_word_tokenize

        # Open files (or just use stdin and stdout)
        fin, fout = open_files(arguments['FILE'], arguments['--output'])

        # Tokenize lines
        try:
            for line in fin:
                fout.write(' '.join(tokenize_fn(line)))
                fout.write('\n')

        # If everything worked so far, this shouldn't happen
        except Exception:  # pylint: disable=W0703
            sys.stderr.write('Error: An unkown error occured during '
                             'tokenization.\n')
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
