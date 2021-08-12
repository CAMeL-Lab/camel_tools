# MIT License
#
# Copyright 2018-2021 New York University Abu Dhabi
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


from collections import namedtuple
import json
import os
from pathlib import Path
import sys


class DataLookupException(ValueError):
    """Exception thrown when an invalid component or dataset is specified in a
    dataset lookup operation.

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
    if sys.platform == 'win32':
        return Path(home, 'AppData/Roaming/camel_tools')
    else:
        return Path(home, '.camel_tools')


CT_DATA_PATH_DEFAULT = _get_appdatadir()
CT_DATA_PATH_DEFAULT.mkdir(parents=True, exist_ok=True)
CT_DATA_DIR = CT_DATA_PATH_DEFAULT

_CATALOGUE_PATH = Path(__file__).parent / 'catalogue.json'
with _CATALOGUE_PATH.open('r', encoding='utf-8') as cat_fp:
    _CATALOGUE = json.load(cat_fp)

if os.environ.get('CAMELTOOLS_DATA') is not None:
    CT_DATA_DIR = Path(
        os.environ.get('CAMELTOOLS_DATA')).expanduser().absolute()

_CT_DATASET_PATH = Path(CT_DATA_DIR, 'data')


_DownloadInfo = namedtuple('DownloadInfo', ['name',
                                            'description',
                                            'type',
                                            'file_id',
                                            'url',
                                            'size',
                                            'destination'])

_ComponentInfo = namedtuple('ComponentInfo', ['name', 'datasets', 'default'])

_DatasetInfo = namedtuple('DatasetInfo', ['component',
                                          'name',
                                          'description',
                                          'license',
                                          'version',
                                          'path'])


class DownloadInfo(_DownloadInfo):
    """Named tuple containing information about a data download.

    Attributes:
        name (:obj:`str`): The name used to query this download.
        description (:obj:`str`): A description of this download.
        type (:obj:`str`): The type of download. Values can be one of the
            following: 'url', 'google-drive'.
        url (:obj:`str`): The URL of the download (used only when `type` is set
            to 'url').
        file_id (:obj:`str`): The file ID of the download (used only when
            `type` is set to 'google-drive').
        size (:obj:`str`): Estimated data size in Bytes, KB, MB, or GB.
        destination (:obj:`str`): The destination of the downloaded file
            relative to the camel-tools data path.
    """


class ComponentInfo(_ComponentInfo):
    """Named tuple containing information about a component.

    Attributes:
        name (:obj:`str`): The name used to query this component.
        datasets (:obj:`frozenset` of :obj:`DatasetInfo`): A set of all
            datasets for this component.
        default (:obj:`str`): Name of the default dataset for this component.
    """


class DatasetInfo(_DatasetInfo):
    """Named tuple containing information about a dataset.

    Attributes:
        component (:obj:`str`): The component name this dataset belongs to.
        name (:obj:`str`): The name used to query this dataset.
        description (:obj:`str`): A description of this dataset.
        license (:obj:`str`): The license this dataset is distributed under.
        version (:obj:`str`): This dataset's version number.
        path (:obj:`Path`): The path to this dataset.
    """


def _gen_catalogue(cat_dict):
    catalogue = {'downloads': {}, 'components': {}}

    # Populate downloads
    for dl_name, dl_info in cat_dict['downloads'].items():
        catalogue['downloads'][dl_name] = DownloadInfo(
            dl_name,
            dl_info.get('description', None),
            dl_info['type'],
            dl_info.get('file_id', None),
            dl_info.get('url', None),
            dl_info['size'],
            dl_info['destination'])

    # Populate components
    for comp_name, comp_info in cat_dict['components'].items():
        datasets = {}

        for ds_name, ds_info in comp_info['datasets'].items():
            ds_path = Path(_CT_DATASET_PATH, ds_info['path'])
            datasets[ds_name] = DatasetInfo(comp_name,
                                            ds_name,
                                            ds_info.get('description', None),
                                            ds_info.get('license', None),
                                            ds_info.get('version', None),
                                            ds_path)

        catalogue['components'][comp_name] = {
            'default': comp_info['default'],
            'datasets': datasets
        }

    return catalogue


class DataCatalogue(object):
    """This class allows querying datasets provided by CAMeL Tools.
    """

    _catalogue = _gen_catalogue(_CATALOGUE)

    @staticmethod
    def get_download_info(download):
        """Get the download entry for a given download name.

        Args:
            download (:obj:`str`): Name of the download to lookup in the
            catalogue.

        Returns:
            :obj:`DownloadInfo`: The catalogue entry associated with the given
            download.

        Raises:
            DataLookupException: If `download` is not a valid download name.
        """

        if download not in DataCatalogue._catalogue['downloads']:
            raise DataLookupException('Undefined download {}.'.format(
                                      repr(download)))
        
        return DataCatalogue._catalogue['downloads'][download]

    @staticmethod
    def downloads_list():
        return [v for _, v in 
                sorted(DataCatalogue._catalogue['downloads'].items())]

    @staticmethod
    def get_component_info(component):
        """Get the catalogue entry for a given component.

        Args:
            component (:obj:`str`): Name of the component to lookup in the
                catalogue.

        Returns:
            :obj:`ComponentInfo`: The catalogue entry associated with the given
            component.

        Raises:
            DataLookupException: If `component` is not a valid component name.
        """

        if component not in DataCatalogue._catalogue['components']:
            raise DataLookupException('Undefined component {}.'.format(
                                      repr(component)))

        comp_info = DataCatalogue._catalogue['components'][component]
        default = comp_info['default']
        datasets = frozenset(comp_info['datasets'].values())

        return ComponentInfo(component, datasets, default)

    @staticmethod
    def get_dataset_info(component, dataset=None):
        """Get the catalogue entry for a given dataset for a given component.

        Args:
            component (:obj:`str`): Name of the component dataset belongs to.
            dataset (:obj:`str`, optional): Name of the dataset for `component`
                to lookup. If None, the entry for the default dataset for
                `component` is returned. Defaults to None.

        Returns:
            :obj:`DatasetInfo`: The catalogue entry associated with the given
            dataset.

        Raises:
            DataLookupException: If `component` is not a valid component name
                or if `dataset` is not a valid dataset name for `component`.
        """
        if component not in DataCatalogue._catalogue['components']:
            raise DataLookupException('Undefined component {}.'.format(
                                      repr(component)))

        comp_info = DataCatalogue._catalogue['components'][component]

        if dataset is None:
            dataset = comp_info['default']
        elif dataset not in comp_info['datasets']:
            raise DataLookupException(
                'Undefined dataset {} for component {}.'.format(
                    repr(dataset), repr(component)))

        return comp_info['datasets'][dataset]
