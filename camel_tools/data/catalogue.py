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


from __future__ import annotations
from enum import Enum
from collections import deque
from genericpath import exists
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Set, List, Mapping
import hashlib
import os
import sys

from pyrsistent import pvector, pmap
from tqdm import tqdm

import camel_tools
from camel_tools.data.downloader import HTTPDownloader


HASH_BLOCK_SIZE = 65536
CATALOGUE_URL = "https://raw.githubusercontent.com/CAMeL-Lab/camel-tools-data/main/catalogue-1.4.json"


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

if os.environ.get('CAMELTOOLS_DATA') is not None:
    CT_DATA_DIR = Path(
        os.environ.get('CAMELTOOLS_DATA')).expanduser().absolute()

CT_VERSIONS_PATH = Path(CT_DATA_DIR, 'versions.json')


def _init_progress(progress_bar, desc, total):
    progress_bar[0] = tqdm(desc=desc,
                           total=total,
                           unit='B',
                           colour='green',
                           unit_scale=True)


def _update_progress(progress_bar, chunk_size):
    progress_bar[0].update(chunk_size)


def _finish_progress(progress_bar):
    progress_bar[0].close()


def _hash_file(path):
    file_hash = hashlib.sha256()

    with path.open('rb') as fp:
        fb = fp.read(HASH_BLOCK_SIZE)

        while len(fb) > 0:
            file_hash.update(fb)
            fb = fp.read(HASH_BLOCK_SIZE)

    return file_hash.hexdigest()


class PackageType(Enum):
    """Enum indicating the type of a package."""

    META = 0
    """Indicates a package is a meta package (ie. contains no files,
    only dependencies)"""

    HTTP = 1
    """Indicates package is a zip file that can be downloaded via
    HTTP/HTTPS."""


@dataclass(frozen=True)
class FileEntry:
    """Data class containing information about a given file.
    """

    path: str
    """Relative path of file in the package directory."""

    sha256: str
    """SHA256 hash of this file."""


@dataclass(frozen=True)
class PackageEntry:
    """Data class containing information about a given package.
    """

    name: str
    """Name of this package."""

    description: str
    """Description of this package"""

    size: Optional[int]
    """Size of this package in bytes. Is `None` for meta packages."""

    version: Optional[str]
    """Package version. Is `None` for meta packages."""

    license: str
    """License this package is distributed under.
    Is `None` for meta packages.
    """

    package_type: PackageType
    """Type of this package."""

    url: Optional[str]
    """URL for downlading this package's zip file.
    Is `None` for meta packages."""

    destination: Optional[Path]
    """Installation path of package. Is `None` for meta packages."""

    dependencies: Optional[Set[str]]
    """Names of packages this package depends on."""

    files: Optional[List[FileEntry]]
    """List of files included in this package. Is `None` for meta packages."""

    private: bool
    """Indicates if this package should be hidden when being listed."""

    sha256: Optional[str]
    """SHA256 hash of package zip file. Is `None` for meta packages."""


@dataclass(frozen=True)
class DatasetEntry:
    """Data class containing information about an individual dataset.
    """

    name: str
    """Name of this dataset."""

    component: str
    """Name of the component this dataset belongs to."""

    path: str
    """Relative path of this dataset in the data directory."""


@dataclass(frozen=True)
class ComponentEntry:
    """Data class that contains dataset information for a given component.
    """

    name: str
    """Name of this component."""

    default: str
    """The default dataset name for this component."""

    datasets: Mapping[str, DatasetEntry]
    """A mapping of dataset names to their respective entries."""


class CatalogueError(Exception):
    """Exception raised when an error occurs during data download.
    """

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


@dataclass(frozen=True)
class Catalogue:
    """This class allows downloading and querying datasets provided by
    CAMeL Tools.
    """

    version: str
    """Catalogue version string."""

    packages: Mapping[str, PackageEntry]
    """Mapping of package names to their respective entries."""

    components: Mapping[str, ComponentEntry]
    """Mapping of component names with their respective entries."""

    @staticmethod
    def get_default_catalogue_path() -> Path:
        """Returns the default catalogue path, respecting the `CAMELTOOLS_DATA`
        environment variable if it is set.

        Returns:
            :obj:`Path`: Path to the catalogue file.
        """
        cat_version = '.'.join(camel_tools.__version__.split('.')[0:2])
        cat_name = f'catalogue.json'

        return Path(CT_DATA_DIR, cat_name)

    @staticmethod
    def update_catalogue():
        """Download latest catalogue for the current version of CAMeL Tools.
        
        Raises:
            :obj:`~camel_tools.data.DownloaderError`: When an error occurs
                while downloading catalogue.
        """

        cat_path = Catalogue.get_default_catalogue_path()
        HTTPDownloader.download(CATALOGUE_URL, cat_path)

    @staticmethod
    def load_catalogue(path: Path=None) -> 'Catalogue':
        """Load catalogue file at a given path.

        Arguments:
            path(:obj:`Path`): Path to catalogue file.

        Returns:
            :obj:`Catalogue`: :obj:`~Catalogue` instance populated by the
            contents of the catalogue file.
        """

        if path is None:
            path = Catalogue.get_default_catalogue_path()

        # Check if catalogue is there
        if not exists(path):
            Catalogue.update_catalogue()

        with path.open('r', encoding='utf-8') as cfp:
            catalogue_json = json.load(cfp)

        version = catalogue_json['version']
        packages = {}
        components = {}

        for pkg_name, pkg_json in catalogue_json['packages'].items():
            if pkg_json.get('files', None) is None:
                files = None
            else:
                files = []
                for file_json in pkg_json['files']:
                    files.append(FileEntry(file_json['path'], file_json['sha256']))
                files = pvector(files)

            destination = pkg_json.get('destination', None)
            if destination is not None:
                destination = Path(CT_DATA_DIR, 'data', destination)

            pkg_entry = PackageEntry(
                name=pkg_name,
                description=pkg_json.get('description', ''),
                version=pkg_json.get('version', None),
                license=pkg_json.get('license', None),
                package_type=PackageType[pkg_json['package_type'].upper()],
                url=pkg_json.get('url', None),
                destination=destination,
                dependencies=frozenset(pkg_json.get('dependencies', [])),
                files=files,
                private=pkg_json['private'],
                sha256=pkg_json.get('sha256', None),
                size=pkg_json.get('size', None)
            )

            packages[pkg_name] = pkg_entry

        for cmp_name, cmp in catalogue_json['components'].items():
            default = cmp['default']
            datasets = {}

            for ds_name, ds in cmp['datasets'].items():
                ds_path = Path(CT_DATA_DIR, 'data', ds['path'])
                datasets[ds_name] = DatasetEntry(ds_name,
                                                 cmp_name,
                                                 ds_path)

            components[cmp_name] = ComponentEntry(cmp_name, default, datasets)

        return Catalogue(version, packages, components)

    def get_package(self, package: str) -> PackageEntry:
        """Get a package entry for a given package name.

        Arguments:
            package (:obj:`str`): Name of package to query.

        Returns:
            :obj:`~camel_tools.data.ComponentEntry`: Entry associated with
            given package name.

        Raises:
            :obj:`~camel_tools.data.CatalogueError`: When `package` is not
                a valid package name.
        """

        if package in self.packages:
            return self.packages[package]
        else:
            raise CatalogueError(f'Invalid package name {repr(package)}.')

    def get_component(self, component: str) -> ComponentEntry:
        """Get component entry for a given component name.

        Arguments:
            component (:obj:`str`): Name of component to query.

        Returns:
            :obj:`~camel_tools.data.PackageEntry`: Entry associated with given
            component name.

        Raises:
            :obj:`~camel_tools.data.CatalogueError`: When `component` is not
                a valid component name.
        """

        if component in self.components:
            return self.components[component]
        else:
            raise CatalogueError(f'Invalid component name {component}.')

    def get_dataset(self, component: str, dataset: str=None) -> DatasetEntry:
        """Get dataset entry for a given component name and dataset name.

        Arguments:
            component (:obj:`str`): Name of component.
            dataset (:obj:`str`, Optional): Name of dataset for given component
                to query. If set to `None` then the entry for the default
                dataset will be returned. Defaults to `None`.

        Returns:
            :obj:`~camel_tools.data.DatasetEntry`: The dataset entry for the
            given component and dataset names.
        """

        if component in self.components:
            cmp = self.components[component]

            if dataset is None:
                dataset = cmp.default
            if dataset in cmp.datasets:
                return cmp.datasets[dataset]
            raise CatalogueError(f'Invalid dataset name {repr(dataset)}.')
        else:
            raise CatalogueError(f'Invalid component name {repr(component)}.')

    def _get_dependencies(self, package: str) -> "frozenset[PackageEntry]":
        dep_set = set()
        dep_stack = deque([package])

        while len(dep_stack) > 0:
            pkg_name = dep_stack.pop()
            pkg = self.packages.get(pkg_name, None)

            if pkg is None:
                raise CatalogueError(f'Invalid package name {repr(pkg_name)}.')

            if pkg.package_type != PackageType.META:
                dep_set.add(pkg_name)

            if pkg.dependencies is None or len(pkg.dependencies) == 0:
                continue
            
            for pkg_dep in pkg.dependencies:
                if pkg_dep not in dep_set:
                    dep_stack.append(pkg_dep)

        return frozenset(dep_set)

    def get_public_packages(self) -> List[str]:
        """Returns a list of all package names marked as public in the
        catalogue.

        Returns:
            :obj:`list` of :obj:`str`: The list of names of all packages marked
            as public.
        """

        pkgs = [p for p in self.packages.values() if p.private == False]
        pkgs.sort(key=lambda p: p.name)

        return pkgs

    def download_package(self,
                         package: str,
                         recursive: bool=True,
                         force: bool=False,
                         print_status: bool=False):
        """Download and install package with a given name.

        Arguments:
            package (:obj:`str`): Name of package to download and install.
            recursive (:obj:`bool`, Optional): If `True`, dependencies are
                recursively installed. Otherwise, only the package contents are
                installed. Defaults to `True`.
            force (:obj:`bool`, Optional): If `True`, packages that are
                already installed and up-to-date will be reinstalled, otherwise
                they are ignored. Defaults to `False`.
            print_status (:obj:`bool`, Optional): If `True`, prints out the
                download status to standard output.
                Defaults to `False`.
        """

        if package not in self.packages:
            raise CatalogueError(f'Invalid package name {repr(package)}')

        if recursive:
            deps = self._get_dependencies(package)
        else:
            deps = [package]

        if CT_VERSIONS_PATH.exists():
            with CT_VERSIONS_PATH.open('r', encoding='utf-8') as versions_fp:
                ct_versions = json.load(versions_fp)
        else:
            ct_versions = {}

        if not force:
            new_deps = []
            for dep in deps:
                dep_ver = self.packages[dep].version
                if dep not in ct_versions or dep_ver != ct_versions[dep]:
                    new_deps.append(dep)
            deps = new_deps

        if len(deps) == 0:
            if print_status:
                print(f'No new packages will be installed.')
            return

        if print_status:
            pkg_repr = ', '.join([repr(d) for d in deps])
            print(f'The following packages will be installed: {pkg_repr}')

        for dep in deps:
            dep_pkg = self.packages[dep]
    
            if dep_pkg.package_type == PackageType.META:
                continue

            on_dl_start = None
            on_dl_update = None
            on_dl_finish = None
            on_uz_start = None
            on_uz_update = None
            on_uz_finish = None

            if print_status:
                dl_progress_bar = [None]
                on_dl_start = (
                    lambda t: _init_progress(dl_progress_bar,
                                            f'Downloading package {repr(dep)}',
                                            t))
                on_dl_update = lambda c: _update_progress(dl_progress_bar, c)
                on_dl_finish = lambda: _finish_progress(dl_progress_bar)

                uz_progress_bar = [None]
                on_uz_start = (
                    lambda t: _init_progress(uz_progress_bar,
                                            f'Extracting package {repr(dep)}',
                                            t))
                on_uz_update = lambda c: _update_progress(uz_progress_bar, c)
                on_uz_finish = lambda: _finish_progress(uz_progress_bar)

            if dep_pkg.package_type == PackageType.HTTP:
                HTTPDownloader.download(dep_pkg.url,
                                       dep_pkg.destination,
                                       is_zip=True,
                                       on_download_start=on_dl_start,
                                       on_download_update=on_dl_update,
                                       on_download_finish=on_dl_finish,
                                       on_unzip_start=on_uz_start,
                                       on_unzip_update=on_uz_update,
                                       on_unzip_finish=on_uz_finish)

            # Update versions file
            ct_versions[dep] = dep_pkg.version
            with CT_VERSIONS_PATH.open('w', encoding='utf-8') as versions_fp:
                json.dump(ct_versions, versions_fp, indent=4)
