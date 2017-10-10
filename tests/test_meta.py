"""
This is a dummy test module to make sure tox and pytest are properly
configured.

This will eventually be removed.
"""

from __future__ import print_function

import os
import camel_tools as camelt
from camel_tools.disambig import camel_disambig


def test_camelToolsVersion():
    assert camel_disambig.__version__ == camelt.__version__
