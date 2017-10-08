from setuptools import setup

CLASSIFIERS = [
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
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
