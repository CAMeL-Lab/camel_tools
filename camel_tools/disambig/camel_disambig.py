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

import sys
from docopt import docopt
import camel_tools as camelt


__version__ = camelt.__version__


def main():  # pragma: no cover
    version = ('CAMeL Tools v{}'.format(__version__))
    arguments = docopt(__doc__, version=version)

    # TODO: Implement camel_disambig

    sys.exit(0)


if __name__ == '__main__':  # pragma: no cover
    main()
