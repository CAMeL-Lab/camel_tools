Getting Started
===============

Installation
------------

You will need Python 3.8 - 3.12 (64-bit) as well as
`the Rust compiler <https://www.rust-lang.org/learn/get-started>`_ installed.

Linux/macOS
~~~~~~~~~~~

You will need to install some additional dependencies on Linux and macOS.
Primarily CMake, and Boost.

On Ubuntu/Debian you can install these dependencies by running:

.. code-block:: bash

   sudo apt-get install cmake libboost-all-dev

On macOS you can install them using Homewbrew by running:

.. code-block:: bash

   brew install cmake boost

.. _linux-macos-install-pip:

Install using pip
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install camel-tools

   # or run the following if you already have camel_tools installed
   pip install camel-tools --upgrade

On Apple silicon Macs you may have to run the following instead:

.. code-block:: bash

   CMAKE_OSX_ARCHITECTURES=arm64 pip install camel-tools

   # or run the following if you already have camel_tools installed
   CMAKE_OSX_ARCHITECTURES=arm64 pip install camel-tools --upgrade

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
   pip install --upgrade .

.. _linux-macos-install-data:

Installing data
^^^^^^^^^^^^^^^

To install the data sets required by CAMeL Tools components run one of the
following:

.. code-block:: bash

   # To install all datasets
   camel_data -i all

   # or just the datasets for morphology and MLE disambiguation only
   camel_data -i light

   # or just the default datasets for each component
   camel_data -i defaults

See :doc:`reference/packages` for a list of all available datasets.

By default, data is stored in ``~/.camel_tools``.
Alternatively, if you would like to install the data in a different location,
you need to set the :code:`CAMELTOOLS_DATA` environment variable to the desired
path.

Add the following to your :code:`.bashrc`, :code:`.zshrc`, :code:`.profile`,
etc:

.. code-block:: bash

   export CAMELTOOLS_DATA=/path/to/camel_tools_data

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
   pip install --upgrade -f https://download.pytorch.org/whl/torch_stable.html camel-tools

.. _windows-install-source:

Install from source
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Clone the repo
   git clone https://github.com/CAMeL-Lab/camel_tools.git
   cd camel_tools

   # Install from source
   pip install -f https://download.pytorch.org/whl/torch_stable.html .
   pip install --upgrade -f https://download.pytorch.org/whl/torch_stable.html .

.. _windows-install-data:

Installing data
^^^^^^^^^^^^^^^

To install the data packages required by CAMeL Tools components, run one of the
following commands:

.. code-block:: bash

   # To install all datasets
   camel_data -i all

   # or just the datasets for morphology and MLE disambiguation only
   camel_data -i light

   # or just the default datasets for each component
   camel_data -i defaults

See :doc:`reference/packages` for a list of all available datasets.

By default, data is stored in
``C:\Users\your_user_name\AppData\Roaming\camel_tools``.
Alternatively, if you would like to install the data in a different location,
you need to set the ``CAMELTOOLS_DATA`` environment variable to the desired
path. Below are the instructions to do so (on Windows 10):

* Press the **Windows** button and type ``env``.
* Click on **Edit the system environment variables (Control panel)**.
* Click on the **Environment Variables...** button.
* Click on the **New...** button under the **User variables** panel.
* Type ``CAMELTOOLS_DATA`` in the **Variable name** input box and the
  desired data path in **Variable value**. Alternatively, you can browse for the
  data directory by clicking on the **Browse Directory...** button.
* Click **OK** on all the opened windows.


Next Steps
----------

To get started, you can follow along
`the Guided Tour <https://colab.research.google.com/drive/1Y3qCbD6Gw1KEw-lixQx1rI6WlyWnrnDS?usp=sharing>`_
for a quick overview of the components provided by CAMeL Tools.

See :doc:`cli_tools` for information on using the command-line tools or 
:doc:`api` for information on using the Python API.
