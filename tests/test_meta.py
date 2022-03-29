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

"""
This is a test module to make sure meta-data in all submodules are set
correctly.
"""

from __future__ import absolute_import, print_function

import os

import camel_tools as camelt
from camel_tools.cli import camel_calima_star
from camel_tools.cli import camel_transliterate
from camel_tools.cli import camel_arclean


VERSION_PATH = os.path.join(os.path.dirname(camelt.__file__), 'VERSION')
with open(VERSION_PATH, 'r', encoding='utf-8') as version_fp:
    VERSION = version_fp.read().strip()


def test_camel_tools_version():
    """Test that all module and CLI script versions are the same as the version
    file.
    """

    assert(VERSION ==
           camelt.__version__ ==
           camel_calima_star.__version__ ==
           camel_transliterate.__version__ ==
           camel_arclean.__version__)
