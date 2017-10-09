"""
This is a dummy test module to make sure tox and pytest are properly
configured.

This will eventually be removed.
"""

from __future__ import print_function

import os
import camel_tools as camelt
from camel_tools.scripts.camel_disambig import camel_disambig


def test_camelToolsVersion():
    version_file = os.path.join(os.path.dirname(__file__),
                                '..',
                                'camel_tools',
                                'VERSION')
    with open(os.path.abspath(version_file), 'r') as infile:
        version = infile.read().strip()

    assert camelt.__version__ == version


def test_camelDisambigVersion():
    version_file = os.path.join(os.path.dirname(__file__),
                                '..',
                                'camel_tools',
                                'scripts',
                                'camel_disambig',
                                'VERSION')
    with open(os.path.abspath(version_file), 'r') as infile:
        version = infile.read().strip()

    assert camel_disambig.__version__ == version
