"""
This is a test module to make sure meta-data in all submodules are set
correctly.
"""

from __future__ import absolute_import, print_function

import os

import camel_tools as camelt
from camel_tools.disambig import camel_disambig
from camel_tools.transliterate import camel_transliterate
from camel_tools.arclean import camel_arclean


VERSION_PATH = os.path.join(os.path.dirname(camelt.__file__), 'VERSION')
with open(VERSION_PATH, 'r') as infile:
    VERSION = infile.read().strip()


def test_camel_tools_version():
    """Test that all module and CLI script versions are the same as the version
    file.
    """

    assert(VERSION ==
           camelt.__version__ ==
           camel_disambig.__version__ ==
           camel_transliterate.__version__ ==
           camel_arclean.__version__)
