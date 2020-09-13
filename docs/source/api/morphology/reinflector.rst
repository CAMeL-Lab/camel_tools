camel_tools.morphology.reinflector
===================================

.. automodule:: camel_tools.morphology.reinflector

Classes
-------

.. autoclass:: camel_tools.morphology.reinflector.Reinflector
   :members:

Examples
--------

.. code-block:: python

   from camel_tools.morphology.database import MorphologyDB
   from camel_tools.morphology.reinflector import Reinflector

   # Initialize database in reinflection mode
   db = MorphologyDB('path/to/database', 'r')

   # Create reinflector instance
   reinflector = Generator(db)

   # Specify word and features to generate for
   word = ''
   features = {}

   # Generate analyses for lemma and features
   analyses = reinflector.reinflect(word, features)
