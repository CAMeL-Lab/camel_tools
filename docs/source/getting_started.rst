Getting Started
===============

Installation
------------

You will need Python 3.6 and above (64-bit).

.. warning::

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


Next Steps
----------

See :doc:`cli_tools` for information on using the command-line tools or 
:doc:`api` for information on using the Python API.
