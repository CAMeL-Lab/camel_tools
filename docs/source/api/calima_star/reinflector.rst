camel_tools.calima_star.reinflector
===================================

The reinflector component of CALIMA Star.

Classes
-------

.. autoclass:: camel_tools.calima_star.reinflector.CalimaStarReinflector
   :members:

Examples
--------

.. code-block:: python

   from camel_tools.calima_star.database import CalimaStarDB
   from camel_tools.calima_star.reinflector import CalimaStarReinflector

   # Initialize database in reinflection mode
   db = CalimaStarDB('path/to/database', 'r')

   # Create reinflector instance
   reinflector = CalimaStarGenerator(db)

   # Specify word and features to generate for
   word = ''
   features = {}

   # Generate analyses for lemma and features
   analyses = reinflector.reinflect(word, features)
