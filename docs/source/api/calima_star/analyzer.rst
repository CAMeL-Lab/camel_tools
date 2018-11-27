camel_tools.calima_star.analyzer
================================

The morphological analyzer component of CALIMA Star.

Globals
-------
.. autodata:: camel_tools.calima_star.analyzer.DEFAULT_NORMALIZE_MAP

Classes
-------

.. autoclass:: camel_tools.calima_star.analyzer.CalimaStarAnalyzer
   :members:

Examples
--------

.. code-block:: python

   from camel_tools.calima_star.database import CalimStarDB
   from camel_tools.calima_star.analyzer import CalimStarAnalyzer

   db = CalimaStarDB('path/to/database', 'a')

   # Create analyzer with no backoff
   analyzer = CalimStarAnalyzer(db)


   # Create analyzer with NOAN_ALL backoff
   analyzer = CalimStarAnalyzer(db, 'NOAN_ALL')

   # or
   analyzer = CalimStarAnalyzer(db, backoff='NOAN_ALL')


   # To analyze a word, we can use the analyze() method
   analyses = analyzer.analyze('شارع')
