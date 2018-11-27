# CAMeL Tools

[![Documentation Status](https://readthedocs.org/projects/camel-tools/badge/?version=latest)](https://camel-tools.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![alt text](camel_logo.png "CAMeL logo")

## Introduction

CAMeL Tools is a suite of morphological analysis and disambiguation tools for
Arabic developed by the
[CAMeL Lab](https://nyuad.nyu.edu/en/research/faculty-research/camel-lab.html)
at [New York University Abu Dhabi](http://nyuad.nyu.edu/).

## Installation

You will need Python 2.7 or Python 3.4 and above.

### Using pip

```bash
pip install camel_tools
```

### From Source

```bash
# Download the repo
git clone https://github.com/owo/camel_tools.git
cd camel_tools

# Install CAMeL Tools and all dependencies
pip install .
```

## Documentation

You can find the
[full online documentation here](https://camel-tools.readthedocs.io) for both
the command-line tools and the Python API.

Alternatively, you can build your own local copy of the documentation as
follows:

```bash
# Install dependencies
pip install sphinx recommonmark sphinx-rtd-theme

# Go to docs subdirectory
cd docs

# Build HTML docs
make html
```

This should compile all the HTML documentation in to `docs/build`.

## LICENSE

CAMeL Tools is available under the MIT license.
See the [LICENSE file](./LICENSE) for more info.

## Contribute

If you would like to contribute to CAMeL Tools, please read the
[CONTRIBUTE.md](./CONTRIBUTING.md) file.

## Contributors

- [Ossama Obeid](https://github.com/owo)
- [Go Inoue](https://github.com/go-inoue)
