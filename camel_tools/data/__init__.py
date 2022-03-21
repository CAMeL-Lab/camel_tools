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


"""This sub-module contains utilities for locating datastes for the various
CAMeL Tools components.
"""


from camel_tools.data.catalogue import Catalogue, DatasetEntry, ComponentEntry
from camel_tools.data.catalogue import CatalogueError, FileEntry, PackageEntry
from camel_tools.data.catalogue import PackageType, CT_DATA_DIR
from camel_tools.data.downloader import DownloaderError


__all__ = [
    'Catalogue',
    'CatalogueError',
    'PackageEntry',
    'PackageType',
    'FileEntry',
    'ComponentEntry',
    'DatasetEntry',
    'DownloaderError',
    'CATALOGUE',
    'CT_DATA_DIR'
]


CATALOGUE = Catalogue.load_catalogue()
