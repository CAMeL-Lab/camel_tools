"""
A suite of morphological analysis and disambiguation tools for Arabic developed
by the CAMeL Lab at New York University Abu Dhabi.
"""

from __future__ import print_function, absolute_import

import os


try:
    version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
    with open(version_file, 'r') as infile:
        __version__ = infile.read().strip()
except Exception:  # pragma: no cover
    __version__ = '???'
