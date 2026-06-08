Morphology Databases Post-installation
======================================

This page provides post-installation instructions for specific morphological database packages that
require additional installation steps.

Post-installation Steps
-----------------------

.. _calima-msa-s31-db-post-install:

calima-msa-s31
^^^^^^^^^^^^^^

1. Install the database by running ``camel_data -i morphology-db-msa-s31``.
2. Purchase a copy SAMA 3.1 from the `Linguistic Data Consortium <https://catalog.ldc.upenn.edu/LDC2010L01>`_.
3. Download the `SAMA 3.1 archive <https://catalog.ldc.upenn.edu/download/91f36443e9aaa1c9f367293485b7528cf9cf15d938fdfb0885d111fb37ec>`_
   (should be called ``LDC2010L01.tgz``).
4. Run ``camel_data -p morphology-db-msa-s31 /path/to/LDC2010L01.tgz``.


Usage
-----

The example below shows how we can now use *calima-msa-s31* after performing the above
post-installation steps.
In this case, we will be using *calima-mas-s31* to diacritize a sentence.

.. code-block:: python

   from camel_tools.morphology.analyzer import Analyzer
   from camel_tools.morphology.database import MorphologyDB
   from camel_tools.disambig.bert import BERTUnfactoredDisambiguator

   # Load the calima-msa-s31 database
   db = MorphologyDB.builtin_db('calima-msa-s31')

   # Create an analyzer instance using the calima-msa-s31 database
   analyzer = Analyzer(db, 'ADD_PROP', cache_size=100000)

   # Load the pretrained MSA BERT disambiguator
   disambig = BERTUnfactoredDisambiguator.pretrained(model_name='msa', pretrained_cache=False)

   # Replace the default analyzer with the calima-msa-s31 analyzer
   disambig.set_analyzer(analyzer)

   # Disambiguate sentence
   sentence = 'سوف نقرأ الكتب'.split()
   sentence_disambig = disambig.disambiguate(sentence)

   # Extract diacritized words
   sentence_diacritized = [d.analyses[0].analysis['diac'] for d in sentence_disambig]
   print(' '.join(sentence_diacritized))
