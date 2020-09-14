camel_tools.dialectid
======================

.. DANGER::
   **Note:** This component is not available on Windows.


.. automodule:: camel_tools.dialectid


Classes
-------

.. autoclass:: camel_tools.dialectid.DIDPred
   :members:
.. autoclass:: camel_tools.dialectid.DialectIdentifier
   :members:
.. autoclass:: camel_tools.dialectid.DialectIdError
   :members:
.. autoclass:: camel_tools.dialectid.UntrainedModelError
   :members:
.. autoclass:: camel_tools.dialectid.InvalidDataSetError
   :members:
.. autoclass:: camel_tools.dialectid.PretrainedModelError
   :members:


Functions
---------

.. autofunction:: camel_tools.dialectid.label_to_dialect
.. autofunction:: camel_tools.dialectid.label_dialect_pairs


Examples
--------

Below is an example of how to load and use the default pre-trained model.

.. code-block:: python

   from camel_tools.dialectid import DialectIdentifier

   did = DialectIdentifier.pretrained()

   sentences = [
       'مال الهوى و مالي شكون اللي جابني ليك  ما كنت انايا ف حالي بلاو قلبي يانا بيك',
       'بدي دوب قلي قلي بجنون بحبك انا مجنون ما بنسى حبك يوم'
   ]

   predictions = did.predict(sentences)

   # Each prediction is a tuple containing both the top prediction and the
   # percentage score of each dialect. To get only the top prediction, we can
   # do the following:
   top_dialects = [p.top for p in predictions]
