camel_tools.morphology.database
================================

The :obj:`.MorphologyDB` class parses a morphology database file and generates
indexes to be used by the analyzer, generator, and reinflector components.
You will never have to access :obj:`.MorphologyDB` instances directly but only
pass them as arguments when creating new instances of the analyzer, generator,
and reinflector components.


Classes
-------

.. autoclass:: camel_tools.morphology.database.MorphologyDB
   :members:


.. _camel_morphology_dbs:

Databases
---------

Below is a list of databases that ship with CAMeL Tools:

* **calima-msa-r13** Database for analyzing Modern Standard Arabic. [#fn1]_
* **calima-egy-r13** Database for analyzing Egyptian Arabic. [#fn2]_
* **calima-glf-01** Database for analyzing Gulf Arabic. [#fn3]_


Examples
--------

.. code-block:: python

   from camel_tools.morphology.database import MorphologyDB

   # Initialize the default database ('calima-msa-r13')
   db = MorphologyDB.builtin_db()

   # In the above call, the database is loaded for analysis only by defaut.
   # This is equivalent to writing:
   db = MorphologyDB.builtin_db(flags='a')

   # We can load it for generation as so:
   db = MorphologyDB.builtin_db(flags='g')

   # Or for reinflection as so:
   db = MorphologyDB.builtin_db(flags='r')

   # Since reinflection uses the database in both analysis and generation modes
   # internally, the above is equivalent to writing:
   db = MorphologyDB.builtin_db(flags='ag')


   # We can initialize other builtin databases by providing the name of the
   # desired database. In the examples above, we loaded the default database
   # 'calima-msa-r13'. We can load other builtin databases by providing the
   # desired databases name. Here we'll load the builtin Egyptian database,
   # 'calima-egy-r13':
   db = MorphologyDB.builtin_db('calima-egy-r13')

   # Or with flags:
   db = MorphologyDB.builtin_db('calima-egy-r13', flags='r')


   # We can also initialize external databases:
   db = MorphologyDB('/path/to/database')

   # or with flags:
   db = MorphologyDB('/path/to/database', flags='g')


.. rubric:: Footnotes

.. [#fn1] **calima-msa-r13** is a modified version of the `almor-msa-r13.db`
   database that ships with
   `MADAMIRA <http://innovation.columbia.edu/technologies/cu14012_arabic-language-disambiguation-for-natural-language-processing-applications>`_.
   The `calima-msa-r13` database is distributed under the
   `GNU General Public License version 2 <https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html#SEC1>`_.

.. [#fn2] **calima-egy-r13** is a modified version of the `almor-cra07.db`
   database that ships with
   `MADAMIRA <http://innovation.columbia.edu/technologies/cu14012_arabic-language-disambiguation-for-natural-language-processing-applications>`_.
   The `calima-egy-r13` database is distributed under the
   `GNU General Public License version 2 <https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html#SEC1>`_.

.. [#fn3] **calima-glf-01** database is distributed under the
   `the Creative Commons Attribution 4.0 International License <http://creativecommons.org/licenses/by/4.0/>`_.
