# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


VERSION_FILE = os.path.join(os.path.dirname(__file__),
                            'camel_tools',
                            'VERSION')
with open(VERSION_FILE) as fh:
    VERSION = fh.read().strip()


CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Environment :: Console',
    'Natural Language :: Arabic',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: Linguistic',
]

DESCRIPTION = ('A suite of morphological analysis and disambiguation tools '
               'for Arabic developed by the CAMeL Lab at New York University '
               'Abu Dhabi.')

LONG_DESCRIPTION = codecs.open('README.md', 'r', encoding='utf-8').read()

INSTALL_REQUIRES = [
    'future',
    'six',
    'docopt',
    'regex'
]

setup(
    name='camel_tools',
    version=VERSION,
    author='Ossama W. Obeid',
    author_email='oobeid@nyu.edu',
    maintainer='Ossama W. Obeid',
    maintainer_email='oobeid@nyu.edu',
    packages=['camel_tools',
              'camel_tools.transliterate',
              'camel_tools.utils'],
    package_data={
        'camel_tools.utils': ['charmaps/*.json'],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            ('camel_disambig='
             'camel_tools.disambig.camel_disambig:main'),
            ('camel_transliterate='
             'camel_tools.transliterate.camel_transliterate:main'),
            ('camel_arclean='
             'camel_tools.arclean.camel_arclean:main'),
        ],
    },
    url='https://github.com/owo/CAMeL_Tools',
    license='UNLICENSED',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
)
