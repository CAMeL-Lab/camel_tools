#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The CAMeL Tools Arabic cleaning utility.

Usage:
    camel_calima_star (-d DATABASE | --db=DATABASE)
                      [-o OUTPUT | --output=OUTPUT] [FILE]
    camel_calima_star (-v | --version)
    camel_calima_star (-h | --help)

Options:
  -d DATABASE --db=DATABASE   CalimaStar database to use.
  -o OUTPUT --output=OUTPUT   Output file. If not specified, output will be
                              printed to stdout.
  -h --help                   Show this screen.
  -v --version                Show version.
"""

from __future__ import absolute_import

import sys
import unicodedata
import re
import collections

from docopt import docopt

import camel_tools as camelt
from camel_tools.utils import CharMapper
from camel_tools.calima_star.database import CalimaStarDB
from camel_tools.calima_star.analyzer import CalimaStarAnalyzer


__version__ = camelt.__version__


_ALL_PUNCT = ''.join(chr(x) for x in range(65536)
                    if unicodedata.category(chr(x))[0] in ['P', 'S'])
_RE_TOKENIZE = re.compile('[' + re.escape(_ALL_PUNCT) + ']|\w+')


def _tokenize(s):
    return s.split()


def _open_files(finpath, foutpath):
    if finpath is None:
        fin = sys.stdin
    else:
        try:
            fin = open(finpath, 'r')
        except Exception:
            sys.stderr.write('Error: Couldn\'t open input file {}.'
                             '\n'.format(repr(finpath)))
            sys.exit(1)

    if foutpath is None:
        fout = sys.stdout
    else:
        try:
            fout = open(foutpath, 'w')
        except Exception:
            sys.stderr.write('Error: Couldn\'t open output file {}.'
                             '\n'.format(repr(foutpath)))
            if finpath is not None:
                fin.close()
            sys.exit(1)

    return fin, fout


def _serialize_analyses(fout, word, analyses, order):
    buff = collections.deque()
    buff.append('#WORD: {}'.format(word))
    if len(analyses) == 0:
        buff.append('NO_ANALYSIS')
    else:
        sub_buff = set()
        for a in analyses:
            output = ' '.join(['{}:{}'.format(f, a[f]) for f in order if f in a])
            sub_buff.add(output)
        buff.extend(sub_buff)

    return '\n'.join(buff)


def main():  # pragma: no cover
    version = ('CAMeL Tools v{}'.format(__version__))
    arguments = docopt(__doc__, version=version)

    # Open files (or just use stdin and stdout)
    fin, fout = _open_files(arguments['FILE'], arguments['--output'])

    # FIXME: Handle FileNotFoundError and other Database errors
    db = CalimaStarDB(arguments['--db'])

    # FIXME: Handle Analyzer errors
    analyzer = CalimaStarAnalyzer(db)

    memoize_table = {}

    for line in fin:
        tokens = _tokenize(line.strip())
        for token in tokens:
            if token in memoize_table:
                fout.write(memoize_table[token])
                fout.write('\n\n')
            else:
                analyses = analyzer.analyze(token)
                serialized = _serialize_analyses(fout, token, analyses,
                                                 db.order)
                memoize_table[token] = serialized
                fout.write(serialized)
                fout.write('\n\n')


if __name__ == '__main__':
    main()
