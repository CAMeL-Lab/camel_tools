# -*- coding: utf-8 -*-

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

import os
from setuptools import setup


VERSION_FILE = os.path.join(os.path.dirname(__file__),
                            'camel_tools',
                            'VERSION')
with open(VERSION_FILE) as fh:
    VERSION = fh.read().strip()


CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: Arabic',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: Linguistic',
]

DESCRIPTION = ('A suite of Arabic natural language processing tools developed '
               'by the CAMeL Lab at New York University Abu Dhabi.')

README_FILE = os.path.join(os.path.dirname(__file__), 'README.rst')
with open(README_FILE, 'r') as fh:
    LONG_DESCRIPTION = fh.read().strip()

INSTALL_REQUIRES = [
    'future',
    'six',
    'docopt',
    'cachetools'
]

setup(
    name='camel_tools',
    version=VERSION,
    author='Ossama W. Obeid',
    author_email='oobeid@nyu.edu',
    maintainer='Ossama W. Obeid',
    maintainer_email='oobeid@nyu.edu',
    packages=['camel_tools',
              'camel_tools.cli',
              'camel_tools.utils',
              'camel_tools.calima_star',
              'camel_tools.disambig',
              'camel_tools.tokenizers'],
    package_data={
        'camel_tools.utils': ['charmaps/*.json'],
        'camel_tools.calima_star': ['databases/*/*.db', 'databases/*/LICENSE']
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            ('camel_transliterate='
             'camel_tools.cli.camel_transliterate:main'),
            ('camel_arclean='
             'camel_tools.cli.camel_arclean:main'),
            ('camel_calima_star='
             'camel_tools.cli.camel_calima_star:main'),
        ],
    },
    url='https://github.com/CAMeL-Lab/CAMeL_Tools',
    license='MIT',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
)
