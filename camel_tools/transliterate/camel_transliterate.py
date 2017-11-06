#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The CAMeL Tools transliteration utility.

Usage:
    camel_transliterate (-s SCHEME | --scheme=SCHEME)
                        [-m MARKER | --marker=MARKER]
                        [-I | --ignore-markers]
                        [-S | --strip-markers]
                        [-o OUTPUT | --output=OUTPUT] [FILE]
    camel_transliterate (-l | --list)
    camel_transliterate (-v | --version)
    camel_transliterate (-h | --help)

Options:
  -s SCHEME --scheme          Scheme used for transliteration.
  -o OUTPUT --output=OUTPUT   Output file. If not specified, output will be
                              printed to stdout.
  -m MARKER --marker=MARKER   Marker used to prefix tokens not to be
                              transliterated. Set to '@@IGNORE@@' by default.
  -I --ignore-markers         Transliterate marked words as well.
  -S --strip-markers          Remove markers in output.
  -l --list                   Show a list of available transliteration schemes.
  -h --help                   Show this screen.
  -v --version                Show version.
"""

from __future__ import print_function, absolute_import

import sys

from docopt import docopt

import camel_tools as camelt
from camel_tools.utils import CharMapper
from camel_tools.transliterate import Transliterator


__version__ = camelt.__version__


_BUILTIN_SCHEMES = [
    ('ar2bw', 'Arabic to Buckwalter'),
    ('ar2safebw', 'Arabic to Safe Buckwalter'),
    ('ar2xmlbw', 'Arabic to XML Buckwalter'),
    ('ar2hsb', 'Arabic to Habash-Soudi-Buckwalter'),
    ('bw2ar', 'Buckwalter to Arabic'),
    ('safebw2ar', 'Safe Buckwalter to Arabic'),
    ('xmlbw2ar', 'XML Buckwalter to Arabic'),
    ('hsb2ar', 'Habash-Soudi-Buckwalter to Arabic'),
]


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


def main():  # pragma: no cover
    version = ('CAMeL Tools v{}'.format(__version__))
    arguments = docopt(__doc__, version=version)

    if arguments['--list']:
        for scheme in _BUILTIN_SCHEMES:
            print("{}   {}".format(scheme[0].ljust(10), scheme[1]))
        sys.exit(0)

    if arguments['--scheme'] is not None:
        if arguments['--scheme'] not in [s[0] for s in _BUILTIN_SCHEMES]:
            sys.stderr.write('Error: {} is not a valid scheme.\n'
                             'Run `camel_transliterate -l` to see the list of '
                             'available schemes.'
                             '\n'.format(repr(arguments['--scheme'])))
            sys.exit(1)

        if arguments['--marker'] is None:
            marker = '@@IGNORE@@'
        else:
            marker = arguments['--marker']

        ignore_markers = arguments['--ignore-markers']
        strip_markers = arguments['--strip-markers']

        # Open files (or just use stdin and stdout)
        fin, fout = _open_files(arguments['FILE'], arguments['--output'])

        try:
            mapper = CharMapper.builtin_mapper(arguments['--scheme'])
            trans = Transliterator(mapper, marker)

            for line in fin:
                fout.write(
                    trans.transliterate(line, strip_markers, ignore_markers)
                )
            fout.flush()

        # If everything worked so far, this shouldn't happen
        except Exception:
            sys.stderr.write('Error: An error occured during '
                             'transliteration.\n')
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
