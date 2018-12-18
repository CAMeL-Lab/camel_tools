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

   from camel_tools.calima_star.database import CalimaStarDB
   from camel_tools.calima_star.analyzer import CalimaStarAnalyzer

   db = CalimaStarDB('path/to/database', 'a')

   # Create analyzer with no backoff
   analyzer = CalimaStarAnalyzer(db)


   # Create analyzer with NOAN_ALL backoff
   analyzer = CalimaStarAnalyzer(db, 'NOAN_ALL')

   # or
   analyzer = CalimaStarAnalyzer(db, backoff='NOAN_ALL')


   # To analyze a word, we can use the analyze() method
   analyses = analyzer.analyze('شارع')
