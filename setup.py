from setuptools import setup

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

setup(
    name='camel_tools',
    version='0.1.0',
    author='Ossama W. Obeid',
    author_email='oobeid@nyu.edu',
    packages=['camel_tools'],
    scripts=[],
    url='https://github.com/owo/CAMeL_Tools',
    license='UNLICENSED',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
)
