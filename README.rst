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

.. image:: camel_logo.png
   :target: camel_logo.png
   :alt: CAMeL Lab Logo

Introduction
------------

CAMeL Tools is  suite of Arabic natural language processing tools developed by
the
`CAMeL Lab <https://nyuad.nyu.edu/en/research/faculty-research/camel-lab.html>`_
at `New York University Abu Dhabi <http://nyuad.nyu.edu/>`_.

Installation
------------

You will need Python 2.7 or Python 3.4 and above.

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
