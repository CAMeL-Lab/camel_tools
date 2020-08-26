camel_tools.disambig.mle
========================

.. automodule:: camel_tools.disambig.mle

Classes
-------

.. autoclass:: camel_tools.disambig.mle.MLEDisambiguator
   :members:


Examples
--------

Below is an example of how to load and use the default pre-trained MLE model
to disambiguate words in a sentence.

.. code-block:: python

   from camel_tools.disambig.mle import MLEDisambiguator

   mle = MLEDisambiguator.pretrained()

   # We expect a sentence to be whitespace/punctuation tokenized beforehand.
   # We provide a simple whitespace and punctuation tokenizer as part of camel_tools.
   # See camel_tools.tokenizers.word.simple_word_tokenize.
   sentence = ['سوف', 'نقرأ', 'الكتب']

   disambig = mle.disambiguate(sentence)

   # Let's, for example, use the top disambiguations to generate a diacritized 
   # version of the above sentence.
   # Note that, in practice, you'll need to make sure that each word has a
   # non-zero list of analyses.
   diacritized = [d.analyses[0].analysis['diac'] for d in disambig]
   print(' '.join(diacritized))
