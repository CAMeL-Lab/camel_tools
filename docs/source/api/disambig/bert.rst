camel_tools.disambig.bert
=========================

.. automodule:: camel_tools.disambig.bert

Classes
-------

.. autoclass:: camel_tools.disambig.bert.BERTUnfactoredDisambiguator
   :members:


Examples
--------

Below is an example of how to load and use the default pre-trained CAMeLBERT
based model to disambiguate words in a sentence.

.. code-block:: python

   from camel_tools.disambig.bert import BERTUnfactoredDisambiguator

   unfactored = BERTUnfactoredDisambiguator.pretrained()

   # We expect a sentence to be whitespace/punctuation tokenized beforehand.
   # We provide a simple whitespace and punctuation tokenizer as part of camel_tools.
   # See camel_tools.tokenizers.word.simple_word_tokenize.
   sentence = ['سوف', 'نقرأ', 'الكتب']

   disambig = unfactored.disambiguate(sentence)

   # Let's, for example, use the top disambiguations to generate a diacritized 
   # version of the above sentence.
   # Note that, in practice, you'll need to make sure that each word has a
   # non-zero list of analyses.
   diacritized = [d.analyses[0].analysis['diac'] for d in disambig]
   print(' '.join(diacritized))
