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

CAMeL Tools is  suite of Arabic natural language processing tools developed by
the
`CAMeL Lab <http://camel-lab.com>`_
at `New York University Abu Dhabi <http://nyuad.nyu.edu/>`_.

    **Please use** `GitHub Issues <https://github.com/CAMeL-Lab/camel_tools/issues>`_
    **to report a bug or if you need help using CAMeL Tools.**


Installation
------------

You will need Python 3.6 and above (64-bit).

Linux/macOS
~~~~~~~~~~~

.. _linux-macos-install-pip:

Install using pip
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install camel-tools --no-deps
   pip install camel-tools

   # or run the following if you already have camel_tools installed
   pip uninstall camel-tools -y
   pip install camel-tools --upgrade --force-reinstall --no-deps
   pip install camel-tools

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

First, download either the
`Full data zip <https://drive.google.com/file/d/1LbU8IefOziwYkTpvyCnX_OgaBJCyU6RG/view?usp=sharing>`_
or the `Light data zip <https://drive.google.com/file/d/1K_xYXN1T5GGMDGX25KElVBXp4EEmjG5R/view?usp=sharing>`_
(see `Datasets <#datasets>`_ for a comparison).

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

First, download either the
`Full data zip <https://drive.google.com/file/d/1LbU8IefOziwYkTpvyCnX_OgaBJCyU6RG/view?usp=sharing>`_
or the `Light data zip <https://drive.google.com/file/d/1K_xYXN1T5GGMDGX25KElVBXp4EEmjG5R/view?usp=sharing>`_
(see `Datasets <#datasets>`_ for a comparison).

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


Datasets
--------

We provide two data distributions for use with CAMeL Tools:
`Full <https://drive.google.com/file/d/1LbU8IefOziwYkTpvyCnX_OgaBJCyU6RG/view?usp=sharing>`_
and `Light <https://drive.google.com/file/d/1K_xYXN1T5GGMDGX25KElVBXp4EEmjG5R/view?usp=sharing>`_.

While the Full archive provides data for all components in CAMeL Tools,
the Light archive contains data for use with the morphological analyzer, the
MLE Disambiguator, and any other components that depend on them only.

Below is a table comparing the feature set included in each release.

+--------------------------+--------+-------+
|                          |  Full  | Light |
+==========================+========+=======+
| Size                     | 1.8 GB | 19 MB |
+--------------------------+--------+-------+
| Morphology               |   ✓    |   ✓   |
+--------------------------+--------+-------+
| Disambiguation           |   ✓    |   ✓   |
+--------------------------+--------+-------+
| Taggers                  |   ✓    |   ✓   |
+--------------------------+--------+-------+
| Tokenization             |   ✓    |   ✓   |
+--------------------------+--------+-------+
| Dialect Identification   |   ✓    |       |
+--------------------------+--------+-------+
| Sentiment Analysis       |   ✓    |       |
+--------------------------+--------+-------+
| Named Entity Recognition |   ✓    |       |
+--------------------------+--------+-------+


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


Citation
--------

If you find CAMeL Tools useful in your research, please cite our paper:

.. code-block:: bibtex

   @inproceedings{obeid-etal-2020-camel,
      title = "{CAM}e{L} Tools: An Open Source Python Toolkit for {A}rabic Natural Language Processing",
      author = "Obeid, Ossama  and
         Zalmout, Nasser  and
         Khalifa, Salam  and
         Taji, Dima  and
         Oudah, Mai  and
         Alhafni, Bashar  and
         Inoue, Go  and
         Eryani, Fadhl  and
         Erdmann, Alexander  and
         Habash, Nizar",
      booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
      month = may,
      year = "2020",
      address = "Marseille, France",
      publisher = "European Language Resources Association",
      url = "https://www.aclweb.org/anthology/2020.lrec-1.868",
      pages = "7022--7032",
      abstract = "We present CAMeL Tools, a collection of open-source tools for Arabic natural language processing in Python. CAMeL Tools currently provides utilities for pre-processing, morphological modeling, Dialect Identification, Named Entity Recognition and Sentiment Analysis. In this paper, we describe the design of CAMeL Tools and the functionalities it provides.",
      language = "English",
      ISBN = "979-10-95546-34-4",
   }


License
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
