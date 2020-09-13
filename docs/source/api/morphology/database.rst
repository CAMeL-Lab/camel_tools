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
   db = MorphologyDB.builtin_db('almor-msa-ext', 'a')

   # or if we want to use the default builtin database (ie. 'almor-msa-ext')
   db = MorphologyDB.builtin_db(flags='g')

   # or just the following if we want the default database in analysis mode
   db = MorphologyDB.builtin_db()
