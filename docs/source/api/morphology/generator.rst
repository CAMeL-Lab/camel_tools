camel_tools.morphology.generator
=================================

.. automodule:: camel_tools.morphology.generator

Classes
-------

.. autoclass:: camel_tools.morphology.generator.Generator
   :members:

Examples
--------

.. code-block:: python

   from camel_tools.morphology.database import MorphologyDB
   from camel_tools.morphology.generator import Generator

   # Initialize database in generation mode
   db = DB('path/to/database', 'g')

   # Create generator instance
   generator = Generator(db)

   # Specify lemma and features to generate for
   lemma = ''
   features = {}

   # Generate analyses for lemma and features
   analyses = generator.generate(lemma, features)
