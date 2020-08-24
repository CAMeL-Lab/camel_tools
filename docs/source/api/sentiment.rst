camel_tools.sentiment
======================

.. automodule:: camel_tools.sentiment


Classes
-------

.. autoclass:: camel_tools.sentiment.SentimentAnalyzer
   :members:


Examples
--------

Below is an example of how to load and use the default pre-trained model.

.. code-block:: python

   from camel_tools.sentiment import SentimentAnalyzer

   sa = SentimentAnalyzer.pretrained()

   # Predict the sentiment of a single sentence
   sentiment = sa.predict_sentence('أنا بخير')

   # Predict the sentiment of multiple sentences
   sentences = [
       'أنا بخير',
       'أنا لست بخير'
   ]
   sentiments = sa.predict(sentences)
