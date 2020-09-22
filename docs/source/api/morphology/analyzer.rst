camel_tools.morphology.analyzer
================================

.. automodule:: camel_tools.morphology.analyzer

Globals
-------
.. autodata:: camel_tools.morphology.analyzer.DEFAULT_NORMALIZE_MAP
   :annotation:

Classes
-------

.. autoclass:: camel_tools.morphology.analyzer.AnalyzedWord
   :members:

.. autoclass:: camel_tools.morphology.analyzer.Analyzer
   :members:

Examples
--------

.. code-block:: python

   from camel_tools.morphology.database import MorphologyDB
   from camel_tools.morphology.analyzer import Analyzer

   db = MorphologyDB.builtin_db()

   # Create analyzer with no backoff
   analyzer = Analyzer(db)


   # Create analyzer with NOAN_PROP backoff
   analyzer = Analyzer(db, 'NOAN_PROP')

   # or
   analyzer = Analyzer(db, backoff='NOAN_PROP')


   # To analyze a word, we can use the analyze() method
   analyses = analyzer.analyze('شارع')
