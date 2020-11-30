#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2020 New York University Abu Dhabi
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
    camel_data [-d <DIR> | --data-dir=<DIR>] <PACKAGE>
    camel_data (-l | --list)
    camel_data (-v | --version)
    camel_data (-h | --help)

Options:
  -l --list
        Show a list of packages available for download.
  -h --help
        Show this screen.
  -v --version
        Show version.
"""


import sys

from docopt import docopt

import camel_tools
from camel_tools.data import DataCatalogue, CT_DATA_DIR
from camel_tools.data.downloader import DataDownloader, DownloaderError


__version__ = camel_tools.__version__


def main():  # pragma: no cover
    try:
        version = ('CAMeL Tools v{}'.format(__version__))
        arguments = docopt(__doc__, version=version)

        if arguments['--list']:
            for dl in DataCatalogue.downloads_list():
                print("{}\t{}\t{}".format(dl.name, dl.size, dl.description))
            sys.exit(0)

        package_name = arguments.get('<PACKAGE>', None)

        try:
            dl_info = DataCatalogue.get_download_info(package_name)
        except:
            sys.stderr.write('Error: Invalid package name. Run `camel_data -l`'
                             ' to get a list of available packages.\n')
            sys.exit(1)

        try:
            DataDownloader.download(dl_info)
        except DownloaderError as e:
            sys.stderr.write('Error: {}\n'.format(e.msg))
            sys.exit(1)

    except KeyboardInterrupt:
        sys.stderr.write('Exiting...\n')
        sys.exit(1)

    except Exception:
        sys.stderr.write('Error: An unknown error occurred.\n')
        sys.exit(1)


if __name__ == '__main__':  # pragma: no cover
    main()
