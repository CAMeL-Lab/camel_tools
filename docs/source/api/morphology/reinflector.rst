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
   db = MorphologyDB.builtin_db(flags='r')

   # Create reinflector instance
   reinflector = Reinflector(db)

   # Specify word and features to generate for
   word = 'شوارع'
   features = {
       'gen': 'm',
       'num': 'd',
       'prc1': 'bi_prep'
   }

   # Generate analyses for lemma and features
   analyses = reinflector.reinflect(word, features)
