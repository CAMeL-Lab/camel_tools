camel_tools.calima_star.generator
=================================

The generator component of CALIMA Star.

Classes
-------

.. autoclass:: camel_tools.calima_star.generator.CalimaStarGenerator
   :members:

Examples
--------

.. code-block:: python

   from camel_tools.calima_star.database import CalimStarDB
   from camel_tools.calima_star.generator import CalimStarGenerator

   # Initialize database in generation mode
   db = CalimaStarDB('path/to/database', 'g')

   # Create generator instance
   generator = CalimStarGenerator(db)

   # Specify lemma and features to generate for
   lemma = ''
   features = {}

   # Generate analyses for lemma and features
   analyses = generator.generate(lemma, features)
