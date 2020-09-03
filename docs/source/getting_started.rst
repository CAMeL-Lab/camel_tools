Getting Started
===============

Installation
------------

You will need Python 3.6 and above.

Using pip
^^^^^^^^^

.. code-block:: bash

   pip install camel_tools

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

Next Steps
----------

See :doc:`cli_tools` for information on using the command-line tools or 
:doc:`api` for information on using the Python API.
