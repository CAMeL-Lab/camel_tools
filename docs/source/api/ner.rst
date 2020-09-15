camel_tools.ner
===============

.. automodule:: camel_tools.ner


Classes
-------

.. autoclass:: camel_tools.ner.NERecognizer
   :members:


Examples
--------

Below is an example of how to load and use the default pre-trained model.

.. code-block:: python

   from camel_tools.ner import NERecognizer

   ner = NERecognizer.pretrained()

   # Predict the labels of a single sentence.
   # The sentence must be pretokenized by whitespace and punctuation.
   sentence = 'إمارة أبوظبي هي إحدى إمارات دولة الإمارات العربية المتحدة السبع .'.split()
   labels = ner.predict_sentence(sentence)

   # Print the list of token-label pairs
   print(list(zip(sentence, labels)))
