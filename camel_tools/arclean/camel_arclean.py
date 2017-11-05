#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The CAMeL Tools Arabic cleaning utility.

Usage:
    camel_arclean [-o OUTPUT | --output=OUTPUT] [FILE]
    camel_arclean (-v | --version)
    camel_arclean (-h | --help)

Options:
  -o OUTPUT --output=OUTPUT   Output file. If not specified, output will be
                              printed to stdout.
  -h --help                   Show this screen.
  -v --version                Show version.
"""

from __future__ import print_function, absolute_import

import sys

from docopt import docopt

import camel_tools as camelt
from camel_tools.utils import CharMapper


__version__ = camelt.__version__


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


def _arclean(mapper, fin, fout):
    for line in fin:
        fout.write(mapper.map_string(line))
    fout.flush()


def main():  # pragma: no cover
    version = ('CAMeL Tools v{}'.format(__version__))
    arguments = docopt(__doc__, version=version)

    # Open files (or just use stdin and stdout)
    fin, fout = _open_files(arguments['FILE'], arguments['--output'])

    try:
        mapper = CharMapper.builtin_mapper('arclean')
        _arclean(mapper, fin, fout)

     # If everything worked so far, this shouldn't happen
    except Exception:
        sys.stderr.write('Error: An error occured during cleaning.\n')
        fin.close()
        fout.close()
        sys.exit(1)

        # Cleanup
        if arguments['FILE'] is not None:
            fin.close()
        if arguments['--output'] is not None:
            fout.close()

    sys.exit(0)


if __name__ == '__main__':  # pragma: no cover
    main()
