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


import os
from setuptools import setup
import sys


VERSION_FILE = os.path.join(os.path.dirname(__file__),
                            'camel_tools',
                            'VERSION')
with open(VERSION_FILE, encoding='utf-8') as version_fp:
    VERSION = version_fp.read().strip()


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: Arabic',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: Linguistic',
]

DESCRIPTION = ('A suite of Arabic natural language processing tools developed '
               'by the CAMeL Lab at New York University Abu Dhabi.')

README_FILE = os.path.join(os.path.dirname(__file__), 'README.rst')
with open(README_FILE, 'r', encoding='utf-8') as version_fp:
    LONG_DESCRIPTION = version_fp.read().strip()

INSTALL_REQUIRES = [
    'future',
    'six',
    'docopt',
    'cachetools',
    'numpy',
    'scipy',
    'pandas',
    'scikit-learn',
    'dill',
    'torch>=1.3',
    'transformers>=3.0.2',
    'editdistance',
    'requests',
    'emoji',
    'pyrsistent',
    'tabulate',
    'tqdm'
]

INSTALL_REQUIRES_NOT_WINDOWS = [
    'camel-kenlm'
]

if sys.platform != 'win32':
    INSTALL_REQUIRES.extend(INSTALL_REQUIRES_NOT_WINDOWS)

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
              'camel_tools.morphology',
              'camel_tools.disambig',
              'camel_tools.disambig.bert',
              'camel_tools.tokenizers',
              'camel_tools.tagger',
              'camel_tools.data',
              'camel_tools.sentiment',
              'camel_tools.dialectid',
              'camel_tools.ner'],
    package_data={
        'camel_tools.utils': ['charmaps/*.json'],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            ('camel_transliterate='
             'camel_tools.cli.camel_transliterate:main'),
            ('camel_arclean='
             'camel_tools.cli.camel_arclean:main'),
            ('camel_morphology='
             'camel_tools.cli.camel_morphology:main'),
            ('camel_dediac='
             'camel_tools.cli.camel_dediac:main'),
            ('camel_word_tokenize='
             'camel_tools.cli.camel_word_tokenize:main'),
            ('camel_diac='
             'camel_tools.cli.camel_diac:main'),
            ('camel_data='
             'camel_tools.cli.camel_data:main'),
        ],
    },
    url='https://github.com/CAMeL-Lab/CAMeL_Tools',
    license='MIT',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.7.0, <3.10.*'
)
