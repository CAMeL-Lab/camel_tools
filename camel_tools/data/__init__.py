# MIT License
#
# Copyright 2018-2019 New York University Abu Dhabi
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


import json
import os
from pathlib import Path
import sys


class DataLookupException(ValueError):
    """Exception thrown when an invalid component or dataset is specified in a
    dataset lookup operation (eg. :meth:`get_dataset_path`).

    Args:
        msg (:obj:`str`): Exception message to be displayed.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def _get_appdatadir():
    home = Path.home()

    # TODO: Make sure this works with OSs other than Windows, Linux and Mac.
    if sys.platform == "win32":
        return Path(home, "AppData/Roaming/camel_tools/data")
    else:
        return Path(home, ".camel_tools/data")


CT_DATA_PATH_DEFAULT = _get_appdatadir()
CT_DATA_PATH_DEFAULT.mkdir(parents=True, exist_ok=True)

_CATALOGUE_PATH = Path(__file__).parent / 'catalogue.json'
with _CATALOGUE_PATH.open('r', encoding='utf-8') as cat_fp:
    _CATALOGUE = json.load(cat_fp)


_CT_DATA_PATH = Path(os.environ.get('CAMELTOOLS_DATA', CT_DATA_PATH_DEFAULT))


# TODO: Wrap this in a class with static methods and a dict like interface
def get_dataset_path(component, dataset=None):
    """Return the path to given dataset for a specific component. It takes into
    consideration the camel_tools data path. by default it's in
    '~/.camel_tools/data' on Unix systems and
    '~/AppData/Roaming/camel_tools/data' on Windows.

    Args:
        component (:obj:`str`): Name of the component
        dataset (:obj:`str`, optional): Name of dataset for given component.
            Defaults to 'default'.

    Raises:
        DataLookupException: When either component or dataset are invalid.

    Returns:
        :obj:`pathlib.Path`: Path to dataset.
    """

    if component not in _CATALOGUE['components']:
        raise DataLookupException('Undefined component {}.'.format(
            repr(component)))

    if dataset is None:
        dataset = _CATALOGUE['components'][component]['default']

    if dataset not in _CATALOGUE['components'][component]['datasets']:
        raise DataLookupException(
            'Undefined dataset {} for component {}.'.format(repr(dataset),
                                                            repr(component)))
    # We assume that the catalogue is internally consistent so we don't need to
    # check if 'path' exists.
    ds_path = _CATALOGUE['components'][component]['datasets'][dataset]['path']

    return Path(_CT_DATA_PATH, ds_path)
