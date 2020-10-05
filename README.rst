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

    **Please use** `GitHub Issues <https://github.com/CAMeL-Lab/camel_tools/issues>`_
    **to report a bug or if you need help using CAMeL Tools.**


Installation
------------

You will need Python 3.6 and above (64-bit).

    CAMeL Tools is still in a pre-release stage and the pip package is
    out-of-date.
    It is therefore recommended to **install from source** until the next
    official release.

Linux/macOS
~~~~~~~~~~~

.. _linux-macos-install-pip:

Install using pip
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install camel-tools

   # or run the following if you already have camel_tools installed
   pip install --upgrade --force-reinstall camel-tools

.. _linux-macos-install-source:

Install from source
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Clone the repo
   git clone https://github.com/CAMeL-Lab/camel_tools.git
   cd camel_tools

   # Install from source
   pip install .

   # or run the following if you already have camel_tools installed
   pip install --upgrade --force-reinstall .

.. _linux-macos-install-data:

Installing data
^^^^^^^^^^^^^^^

First, download the
`zipped data <https://drive.google.com/file/d/1ZtseLpW2vufNdkpruDpbQf28WEw38U5u/view?usp=sharing>`_.

Unzip the file and then move and rename the unzipped directory to
:code:`~/.camel_tools`. If installed correctly, there should be a direct path to
:code:`~/.camel_tools/data`.

Alternatively, if you would like to install the data in a different location,
you need to set the :code:`CAMELTOOLS_DATA` environment variable to the desired
path.

Add the following to your :code:`.bashrc`, :code:`.zshrc`, :code:`.profile`,
etc:

.. code-block:: bash

   export CAMELTOOLS_DATA=/path/to/camel_tools_data

Again, :code:`data` should be a subdirectory of the path set in
:code:`CAMELTOOLS_DATA`.

Windows
~~~~~~~

**Note:** CAMeL Tools has been tested on Windows 10. The Dialect Identification
component is not available on Windows at this time.

.. _windows-install-pip:

Install using pip
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install camel-tools -f https://download.pytorch.org/whl/torch_stable.html

   # or run the following if you already have camel_tools installed
   pip install --upgrade --force-reinstall -f https://download.pytorch.org/whl/torch_stable.html camel-tools

.. _windows-install-source:

Install from source
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Clone the repo
   git clone https://github.com/CAMeL-Lab/camel_tools.git
   cd camel_tools

   # Install from source
   pip install -f https://download.pytorch.org/whl/torch_stable.html .
   pip install --upgrade --force-reinstall -f https://download.pytorch.org/whl/torch_stable.html .

.. _windows-install-data:

Installing data
^^^^^^^^^^^^^^^

First, download the
`zipped data <https://drive.google.com/file/d/1ZtseLpW2vufNdkpruDpbQf28WEw38U5u/view?usp=sharing>`_.

Unzip the file and then move and rename the unzipped directory to
:code:`C:\Users\your_user_name\AppData\Roaming\camel_tools`.
If installed correctly, there should be a direct path to
:code:`C:\Users\your_user_name\AppData\Roaming\camel_tools\data`.

Alternatively, if you would like to install the data in a different location,
you need to set the :code:`CAMELTOOLS_DATA` environment variable to the desired
path. Below are the instructions to do so (on Windows 10):

* Press the **Windows** button and type :code:`env`.
* Click on **Edit the system environment variables (Control panel)**.
* Click on the **Environment Variables...** button.
* Click on the **New...** button under the **User variables** panel.
* Type :code:`CAMELTOOLS_DATA` in the **Variable name** input box and the
  desired data path in **Variable value**. Alternatively, you can browse for the
  data directory by clicking on the **Browse Directory...** button.
* Click **OK** on all the opened windows.

Again, :code:`data` should be a subdirectory of the path set in
:code:`CAMELTOOLS_DATA`.


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
