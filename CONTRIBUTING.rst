Contributing
============

Thank you for considering to contribute to CAMeL Tools, we appreciate the help
:heart:.
To make sure that we maintain the highest quality of code, we do have to adhere
to some strict guidelines though.
Please read through this document to help you get up and running.

If you would like to report a bug, suggest enhancements, or request a new
feature, jump to the `Issues section <#issues>`_.

Git + GitHub
------------

We use the `Git <https://git-scm.com/>`_ version control system to manage the
development with the repository hosted on `GitHub <https://github.com>`_.
If you are new to Git or GitHub, please read through the
`GitHub Bootcamp <https://help.github.com/categories/bootcamp/>`_ to get up to
speed.
We also recommend you bookmark the
`Pro Git book <https://git-scm.com/book/en/v2>`_ as reference (it even has a
`section on GitHub <https://git-scm.com/book/en/v2/GitHub-Account-Setup-and-Configuration>`_\ ).

If you're already familiar with Git and GitHub, please read
`Submitting Pull Requests <#submitting-pull-requests>`_.

Setting Up a Development Environment
------------------------------------

We recommend installing Python through `pyenv <https://github.com/pyenv/pyenv>`_.
This helps with managing multiple Python versions for testing easily (see the
section on `Tests <#tests>`_\ ).

We also recommend using `virtualenv <https://virtualenv.pypa.io/en/stable/>`_
while developing for CAMeL Tools to insure a clean development environment.

Coding Style Guidelines
-----------------------

For the most part, contributers should adhere to the
`pep8 <https://www.python.org/dev/peps/pep-0008>`_ style guide. Since pep8 is a
bit ambiguous in some cases, we enforce the additional rules below.

If we missed to mention a particular case, you should always follow the below
procedure:

#. See how it's done in the codebase.
#. See what pep8 says and choose something that's close to the codebase.
#. If all else fails, ask :)

It might be worthwhile to check out some tools and text-editor plugins to help
check if your code adheres to pep8, such as:

* `flake8 <https://pypi.python.org/pypi/flake8>`_
* `pylint <https://www.pylint.org/>`_
* `SublimeLinter-pep8 <https://github.com/SublimeLinter/SublimeLinter-pep8>`_ for
  `Sublime Text <https://www.sublimetext.com/>`_
* `linter-python-pep8 <https://atom.io/packages/linter-python-pep8>`_ for
  `Atom <https://atom.io/>`_

Source Files
^^^^^^^^^^^^

All Python source files should be UTF-8 encoded with the UTF-8 header on top
like so:

.. code-block:: python

   # -*- coding: utf-8 -*-

Standalone scripts should also have a hashbang header like so:

.. code-block:: python

   #!/usr/bin/env python
   # -*- coding: utf-8 -*-

Indentation
^^^^^^^^^^^

* Each indentation level is 4 spaces (no tabs).
* Arguments should be aligned with the opening delimiter when possible as in the
  first example
  `pep8 indentation section <https://www.python.org/dev/peps/pep-0008/#indentation>`_.
* If arguments are to be split into multiple lines, there should only be one
  argument per line.

Strings
^^^^^^^

* Always using single-quoted strings except for docstrings (as per
  `pep8`_\ ).
* Use the new string formatting API ``'{}'.format(x)`` instead of ``'%s' % (x,)``
  (\ `see here for more information <https://pyformat.info/>`_\ ).

Naming Conventions
^^^^^^^^^^^^^^^^^^

* Classes are always in camel case (eg. ``SomeClass``\ ).
* Variables, functions, and methods are always written in snake case
  (eg. ``some_var``\ ).
* Constants are always uppercase with underscore as a separator
  (eg. ``SOME_CONSTANT``\ ).
* Private classes, variables, constants, functions, and methods
  (ie. only used within a module or a class) follow the same rules as above but
  are prefixed with a single underscore
  (eg. ``_some_var``\ , ``_SomeClass``\ , ``_SOME_CONSTANT``\ ).

Python 2 and 3 Support
----------------------

Ideally, CAMeL Tools should be able to run on Python 3.8 - 3.12.
`Here's a nice cheat-sheet <http://python-future.org/compatible_idioms.html>`_ of
how to do that.

Tests
-----

We use `pytest <https://docs.pytest.org>`_ to test the CAMeL Tools codebase and
`tox <https://tox.readthedocs.io/en/latest/>`_ to automate tests over different
Python environments.
We also use `pytest-cov <https://pypi.python.org/pypi/pytest-cov/>`_ to provide
coverage reporting of the test suite.

To be able to run the tests, you need to perform some additional steps.
Assuming you have pyenv installed, you can install the different Python
versions used for testing by running the following commands:

.. code-block:: bash

   # Install all the python versions we will test against.
   # Note: This list will change to include more Python versions in the future.
   pyenv install 3.8.19
   pyenv install 3.9.19
   pyenv install 3.10.14
   pyenv install 3.11.9
   pyenv install 3.12.4

   # This generates a .python-version file that helps pyenv automatically determine
   # which python versions are associated with the application.
   pyenv local 3.8.19 3.9.19 3.10.14 3.11.9 3.12.4

You also need to install tox:

.. code-block:: bash

   pip install tox

To run the tests, just run the following command:

.. code-block:: bash

   tox

Submitting Pull Requests
------------------------

All changes to CAMeL Tools must be in the form of pull requests.
If you are unfamiliar with pull requests, please read
`this <https://git-scm.com/book/en/v2/GitHub-Contributing-to-a-Project>`_.

Before submitting a pull request, please make sure you follow the guidelines
below while working on your changes:

* Each pull request should try to accomplish one general task.
* All work should be done on a branch with a descriptive name relating to the
  general task (eg. ``fix_bug_x`` or ``add_feature_y``\ ).
* All commits should be signed
  (\ `see here <https://help.github.com/articles/signing-commits-with-gpg/>`_ for
  more information).
* Each individual commit should accomplish one small sub-task and should be
  explainable in a sentence or two.
* Each commit should have a descriptive commit message.
* You should make sure your code passes all tests before committing.
* Changes to VERSION files are done **only** by the maintainer!

Issues
------

Not all contributions have to do with code.
If you would like to report a bug, suggest enhancements, or request a new
feature, please use the
`issues page <https://github.com/CAMeL-Lab/CAMeL_Tools/issues>`_ to do so.

Please adhere to the following rules when posting a new issue:


* Try not to post duplicate issues. Search through previous issues to see if
  your issue has been posted before.
* Create one issue per bug, enhancement suggestion, or feature request.
* Use appropriate labels to indicate the type of issue you are posting.
* Provide detailed information on the system you are running (operating system,
  Python version, etc.), exact steps to reproduce the issue, sample input
  file(s), and the output produced when submitting bug reports.
