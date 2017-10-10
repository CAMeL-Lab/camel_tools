import os
from setuptools import setup


version_file = os.path.join(os.path.dirname(__file__),
                            'camel_tools',
                            'VERSION')
with open(version_file) as fh:
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
    'Programming Language :: Python :: 3.7',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: Linguistic',
]

DESCRIPTION = ('A suite of morphological analysis and disambiguation tools '
               'for Arabic developed by the CAMeL Lab at New York University '
               'Abu Dhabi.')

LONG_DESCRIPTION = open('README.md', 'rt').read()

INSTALL_REQUIRES = [
    'docopt',
]

setup(
    name='camel_tools',
    version=VERSION,
    author='Ossama W. Obeid',
    author_email='oobeid@nyu.edu',
    maintainer='Ossama W. Obeid',
    maintainer_email='oobeid@nyu.edu',
    packages=['camel_tools'],
    entry_points={
        'console_scripts': [
            ('camel_disambig='
             'camel_tools.disambig.camel_disambig:main'),
        ],
    },
    url='https://github.com/owo/CAMeL_Tools',
    license='UNLICENSED',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
)
