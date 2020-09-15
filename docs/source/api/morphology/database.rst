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


Examples
--------

.. code-block:: python

   from camel_tools.morphology.database import MorphologyDB

   # Initialize database for analysis
   db = MorphologyDB('/path/to/database', 'a')

   # or just
   db = MorphologyDB('/path/to/database')


   # Initialize database for generation
   db = MorphologyDB('/path/to/database', 'g')


   # Initialize database for reinflection
   db = MorphologyDB('/path/to/database', 'r')

   # or the following since reinflection requires both analysis and generation
   # indexes.
   db = MorphologyDB('/path/to/database', 'ag')


   # We can also initialize a builtin database using the same flags as above
   db = MorphologyDB.builtin_db('calima-msa-r13', 'a')

   # or if we want to use the default builtin database (ie. 'calima-msa-r13')
   db = MorphologyDB.builtin_db(flags='g')

   # or just the following if we want the default database in analysis mode
   db = MorphologyDB.builtin_db()


.. rubric:: Footnotes

.. [#fn1] **calima-msa-r13** is a modified version of the `almor-msa-r13.db`
   database that ships with
   `MADAMIRA <http://innovation.columbia.edu/technologies/cu14012_arabic-language-disambiguation-for-natural-language-processing-applications>`_.
   The `calima-msa-r13.db` database is distributed under the
   `GNU General Public License version 2 <https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html#SEC1>`_.

.. [#fn2] **calima-egy-r13** is a modified version of the `almor-cra07.db`
   database that ships with
   `MADAMIRA <http://innovation.columbia.edu/technologies/cu14012_arabic-language-disambiguation-for-natural-language-processing-applications>`_.
   The `calima-egy-r13.db` database is distributed under the
   `GNU General Public License version 2 <https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html#SEC1>`_.
