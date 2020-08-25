CAMeL Tools
===========


.. image:: https://img.shields.io/pypi/v/camel-tools.svg
   :target: https://pypi.org/project/camel-tools
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/camel-tools.svg
   :target: https://pypi.org/project/camel-tools
   :alt: PyPI Python Version

.. image:: https://readthedocs.org/projects/camel-tools/badge/?version=latest
   :target: https://camel-tools.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/l/camel-tools.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT License

|

.. image:: camel_tools_logo.png
   :target: camel_tools_logo.png
   :alt: CAMeL Tools Logo

Introduction
------------

**Note:** Due to the current COVID-19 situation, the 1.0 release of CAMeL Tools
has been delayed.
If you would like to receive an email notification when the release is ready,
please fill out
`this form <https://docs.google.com/forms/d/e/1FAIpQLSfw5QSQrx9sUVGZ3Q5MCb0zVOGXWf6aEUFPo-idQQab8tkoDw/viewform>`_.

CAMeL Tools is  suite of Arabic natural language processing tools developed by
the
`CAMeL Lab <http://camel-lab.com>`_
at `New York University Abu Dhabi <http://nyuad.nyu.edu/>`_.

Installation
------------

You will need Python 3.4 and above.

Using pip
^^^^^^^^^

.. code-block:: bash

   pip install camel-tools

From Source
^^^^^^^^^^^

.. code-block:: bash

   # Download the repo
   git clone https://github.com/CAMeL-Lab/camel_tools.git
   cd camel_tools

   # Install CAMeL Tools and all dependencies
   pip install .

Installing Data
^^^^^^^^^^^^^^^

Some components require additional data installed to be used.

First, download the
`zipped data <https://drive.google.com/file/d/1ZtseLpW2vufNdkpruDpbQf28WEw38U5u/view?usp=sharing>`_.

Unzip the file and then move and rename the unzipped directory to
`~/.camel_tools` on unix-like systems or `~\\AppData\\Roaming\\camel_tools` on
Windows (`~` is the path to your home directory). 
If installed correctly, there should be a direct path to either
`~/.camel_tools/data` or `~\\AppData\\Roaming\\camel_tools\\data`
(`data` is a subdirectory in the unzipped directory).
Windows sometimes creates an extra directory to place unzipped files in, so
make sure you're moving the right directory.

Alternatively, if you would like to install the data in a different location,
you need to set the `CAMELTOOLS_DATA` environment variable to the desired
path. Again, `data` should be a subdirectory of `CAMELTOOLS_DATA`.


Documentation
-------------

You can find the
`full online documentation here <https://camel-tools.readthedocs.io>`_ for both
the command-line tools and the Python API.

Alternatively, you can build your own local copy of the documentation as
follows:

.. code-block:: bash

   # Install dependencies
   pip install sphinx recommonmark sphinx-rtd-theme

   # Go to docs subdirectory
   cd docs

   # Build HTML docs
   make html

This should compile all the HTML documentation in to ``docs/build/html``.

LICENSE
-------

CAMeL Tools is available under the MIT license.
See the `LICENSE file
<https://github.com/CAMeL-Lab/camel_tools/blob/master/LICENSE>`_
for more info.

Contribute
----------

If you would like to contribute to CAMeL Tools, please read the
`CONTRIBUTE.rst
<https://github.com/CAMeL-Lab/camel_tools/blob/master/CONTRIBUTING.rst>`_
file.

Contributors
------------

* `Ossama Obeid <https://github.com/owo>`_
* `Go Inoue <https://github.com/go-inoue>`_
* `Bashar Alhafni <https://github.com/balhafni>`_
* `Salam Khalifa <https://github.com/slkh>`_
* `Dima Taji <https://github.com/dima-taji>`_
* `Nasser Zalmout <https://github.com/nzal>`_
* `Nizar Habash <https://github.com/nizarhabash1>`_
