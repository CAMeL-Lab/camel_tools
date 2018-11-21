# CAMeL Tools

![alt text](camel_logo.png "CAMeL logo")

## Introduction

A suite of morphological analysis and disambiguation tools for Arabic developed
by the
[CAMeL Lab](https://nyuad.nyu.edu/en/research/faculty-research/camel-lab.html)
at [New York University Abu Dhabi](http://nyuad.nyu.edu/).

## Installation

At the moment, CAMeL Tools can only be installed from source by following the
instructions below.

```bash
# Download the repo
git clone https://github.com/owo/camel_tools.git
cd camel_tools

# Install CAMeL Tools and all dependencies
pip install .
```

## Usage

CAMeL Tools are a set of command line interface (CLI) tools as well as a set
of Python libraries. This section will help you get started with both.

### CLI Tools

This section will list all the CLI tools that come bundled with CAMeL Tools and
will explain their usage.

#### camel_transliterate

The `camel_transliterate` tool allows you to transliterate text from one form
to another.

[See here](./docs/cli/camel_transliterate.md) for more information.

#### camel_arclean

The `camel_arclean` utility cleans Arabic text.

[See here](./docs/cli/camel_arclean.md) for more information.

#### camel_calima_star

The `camel_calima_star` utility is a command line interface to the CALIMA Star
morphological analyzer, generator, and reinflector.

[See here](./docs/cli/camel_calima_star.md) for more information.

### Python API

Coming soon...

## LICENSE

CAMeL Tools is available under the MIT license.
See the [LICENSE file](./LICENSE) for more info.

## Contribute

If you would like to contribute to CAMeL Tools, please read the
[CONTRIBUTE.md](./CONTRIBUTING.md) file.

## Contributors

- [Ossama Obeid](https://github.com/owo)
- [Go Inoue](https://github.com/go-inoue)
