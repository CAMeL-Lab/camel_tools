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


"""The CAMeL Tools data download utility.

Usage:
    camel_data (-i | --install) [-f | --force] <PACKAGE>
    camel_data (-l | --list)
    camel_data (-u | --update)
    camel_data (-v | --version)
    camel_data (-h | --help)

Options:
  -l --list
        Show a list of packages available for download.
  -i --install
        Install package.
  -f --force
        Force install package and dependencies.
  -u --update
        Update package list.
  -h --help
        Show this screen.
  -v --version
        Show version.
"""


import sys

from docopt import docopt
import tabulate

import camel_tools
from camel_tools.data import CATALOGUE
from camel_tools.data.catalogue import Catalogue, CatalogueError
from camel_tools.data.downloader import DownloaderError


__version__ = camel_tools.__version__


def _sizeof_fmt(num):
    # Modified from https://stackoverflow.com/a/1094933

    if num is None:
        return ''

    for ndx, unit in enumerate(['', 'k', 'M', 'G']):
        if abs(num) < 1000.0:
            if ndx > 0:
                return f'{num:3.1f} {unit}B'
            else:
                return f'{num:3.0f} B '
        num /= 1000.0

    return f'{num:.1f} GB'


def _print_package_list(catalogue: Catalogue):
    packages = catalogue.get_public_packages()

    header = ['Package Name', 'Size', 'License', 'Description']
    rows = [(p.name,
             _sizeof_fmt(p.size),
             p.license,
             p.description) for p in packages]
    alignment = ('left', 'right', 'left', 'left')

    tabulate.PRESERVE_WHITESPACE = True
    print(tabulate.tabulate(rows,
                            tablefmt='simple',
                            headers=header,
                            colalign=alignment))
    print()
    tabulate.PRESERVE_WHITESPACE = False


def _update_catalogue():
    try:
        sys.stdout.write(f'Updating catalogue... ')
        CATALOGUE.update_catalogue()
        sys.stdout.write(f'done\n')
    except Exception:
        sys.stdout.write(f'failed\n')
        sys.stderr.write(f'Error: Couldn\'t update catalogue.\n')
        sys.exit(1)


def main():  # pragma: no cover
    try:
        version = ('CAMeL Tools v{}'.format(__version__))
        arguments = docopt(__doc__, version=version)

        cat_path = CATALOGUE.get_default_catalogue_path()

        if not cat_path.exists():
            _update_catalogue()

        if arguments['--list']:
            _print_package_list(CATALOGUE)
            sys.exit(0)
        
        if arguments['--update']:
            _update_catalogue()
            sys.exit(0)

        if arguments['--install']:
            package_name = arguments.get('<PACKAGE>', None)

            try:
                CATALOGUE.download_package(package_name,
                                           recursive=True,
                                           force=arguments['--force'],
                                           print_status=True)
                sys.exit(0)
            except CatalogueError as c:
                sys.stderr.write(f'Error: {c.msg}')
                sys.exit(1)
            except DownloaderError as d:
                sys.stderr.write(f'Error: {d.msg}')

    except KeyboardInterrupt:
        sys.stderr.write('Exiting...\n')
        sys.exit(1)

    except Exception:
        sys.stderr.write('Error: An unknown error occurred.\n')
        sys.exit(1)


if __name__ == '__main__':  # pragma: no cover
    main()
