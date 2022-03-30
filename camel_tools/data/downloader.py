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


from genericpath import exists
from pathlib import Path
from tempfile import TemporaryDirectory
from os import urandom, remove
from shutil import move, rmtree
import binascii
import zipfile

import requests
from requests.structures import CaseInsensitiveDict


_STREAM_CHUNK_SIZE = 32768


class DownloaderError(Exception):
    """Exception raised when an error occurs during data download.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


class HTTPDownloader:
    """Class to download shared files from a URL.
    """

    @staticmethod
    def download(url,
                 dst,
                 is_zip=False,
                 on_download_start=None,
                 on_download_update=None,
                 on_download_finish=None,
                 on_download_error=None,
                 on_unzip_start=None,
                 on_unzip_update=None,
                 on_unzip_finish=None,
                 on_unzip_error=None):
        if is_zip:
            if dst.exists() and not dst.is_dir():
                raise DownloaderError(
                    'Destination directory {} is a pre-existing file.'.format(
                        repr(str(dst))))
            else:
                dst.mkdir(parents=True, exist_ok=True)

        with TemporaryDirectory() as tmp_dir:
            # Download data to temporary directory
            fname = str(binascii.b2a_hex(urandom(15)), encoding='utf-8')
            tmp_data_path = Path(tmp_dir, fname)

            HTTPDownloader._save_content(url,
                                         tmp_data_path,
                                         on_start=on_download_start,
                                         on_update=on_download_update,
                                         on_finish=on_download_finish,
                                         on_error=on_download_error)

            if is_zip:
                if dst.exists():
                    rmtree(dst)

                # Extract data to destination directory
                HTTPDownloader._extract_content(tmp_data_path,
                                                dst,
                                                on_start=on_unzip_start,
                                                on_update=on_unzip_update,
                                                on_finish=on_unzip_finish,
                                                on_error=on_unzip_error)
            else:
                if dst.exists():
                    remove(dst)

                move(tmp_data_path, dst)

    @staticmethod
    def _save_content(url,
                      destination,
                      on_start=None,
                      on_update=None,
                      on_finish=None,
                      on_error=None):

        try:
            session = requests.Session()

            headers = CaseInsensitiveDict()
            headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            headers["Pragma"] = "no-cache"
            headers["Expires"] = "0"

            response = session.get(url, stream=True, headers=headers)

            curr_size = 0
            total_size = int(response.headers.get('content-length', 0))

            if on_start is not None:
                on_start(total_size)

            with open(destination, 'wb') as fp:
                for chunk in response.iter_content(_STREAM_CHUNK_SIZE):
                    if chunk:  # filter out keep-alive new chunks
                        fp.write(chunk)
                        chunk_size = len(chunk)
                        curr_size += chunk_size

                        if on_update is not None:
                            on_update(chunk_size)

            if curr_size < total_size:
                if on_error is not None:
                    on_error()
                raise DownloaderError(
                    'Download could not be completed.')

            if on_finish is not None:
                on_finish()

        except OSError:
            if on_error is not None:
                on_error()

            raise DownloaderError(
                'An error occured while downloading data.')

    @staticmethod
    def _extract_content(source,
                         destination,
                         on_start=None,
                         on_update=None,
                         on_finish=None,
                         on_error=None):

        try:
            with zipfile.ZipFile(source, 'r') as zip_fp:
                uncompress_size = sum(
                    (file.file_size for file in zip_fp.infolist()))
                
                if on_start is not None:
                    on_start(uncompress_size)

                # zip_fp.extractall(destination)
                for file in zip_fp.infolist():
                    file_size = file.file_size
                    zip_fp.extract(file, destination)
                    
                    if on_update is not None:
                        on_update(file_size)
        except:
            if on_error is not None:
                on_error()

            raise DownloaderError(
                'An error occured while extracting data.')

        if on_finish is not None:
            on_finish()
