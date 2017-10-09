#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The CAMeL Tools disambiguater for dialectal Arabic.

Usage:
    camel_disambig (-v | --version)
    camel_disambig (-h | --help)

Options:
  -h --help         Show this screen.
  -v --version      Show version.
"""

from __future__ import print_function, absolute_import

import os
import sys
from docopt import docopt
import camel_tools as camelt


try:
    version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
    with open(version_file, 'r') as infile:
        __version__ = infile.read().strip()
except Exception:
    __version__ = '???'


def main():
    version = ('camel_disambig v{} | '
               'CAMeL Tools v{}'.format(__version__, camelt.__version__))
    arguments = docopt(__doc__, version=version)

    # TODO: Implement camel_disambig

    sys.exit(0)


if __name__ == '__main__':
    main()
