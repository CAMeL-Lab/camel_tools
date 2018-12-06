camel_tools.calima_star.database
================================

The :obj:`.CalimaStarDB` class parses a CALIMA Star database file and generates
indexes to be used by the analyzer, generator, and reinflector components.
You will never have to access :obj:`.CalimaStarDB` instances directly but only
pass them as arguments when creating new instances of the analyzer, generator,
and reinflector components.

Classes
-------

.. autoclass:: camel_tools.calima_star.database.CalimaStarDB
   :members:


Examples
--------

.. code-block:: python

   from camel_tools.calima_star.database import CalimStarDB

   # Initialize database for analysis
   db = CalimaStarDB('/path/to/database', 'a')

   # or just
   db = CalimaStarDB('/path/to/database')


   # Initialize database for generation
   db = CalimaStarDB('/path/to/database', 'g')


   # Initialize database for reinflection
   db = CalimaStarDB('/path/to/database', 'r')

   # or the following since reinflection requires both analysis and generation
   # indexes.
   db = CalimaStarDB('/path/to/database', 'ag')


   # We can also initialize a builtin database using the same flags as above
   db = CalimaStarDB.builtin_db('calima-msa', 'a')

   # or if we want to use the default builtin database (ie. 'calima-msa')
   db = CalimaStarDB.builtin_db(flags='g')

   # or just the following if we want the default database in analysis mode
   db = CalimaStarDB.builtin_db()
