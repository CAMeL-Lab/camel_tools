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
.. autoclass:: camel_tools.dialectid.DIDModel26
   :members: predict, pretrained
.. autoclass:: camel_tools.dialectid.DIDModel6
   :members: predict, pretrained
.. autoclass:: camel_tools.dialectid.DialectIdError
   :members:
.. autoclass:: camel_tools.dialectid.UntrainedModelError
   :members:
.. autoclass:: camel_tools.dialectid.InvalidDataSetError
    :members:
.. autoclass:: camel_tools.dialectid.PretrainedModelError
   :members:


.. _dialectid_labels:

Labels
------

Below is a table mapping output labels to their respective city, country, and
region dialects:

.. list-table::
   :header-rows: 1

   * - Label
     - City
     - Country
     - Region
   * - ALE
     - Aleppo
     - Syria
     - Levant
   * - ALG
     - Algiers
     - Algeria
     - Maghreb
   * - ALX
     - Alexandria
     - Egypt
     - Nile Basin
   * - AMM
     - Amman
     - Jordan
     - Levant
   * - ASW
     - Aswan
     - Egypt
     - Nile Basin
   * - BAG
     - Baghdad
     - Iraq
     - Iraq
   * - BAS
     - Basra
     - Iraq
     - Iraq
   * - BEI
     - Beirut
     - Lebanon
     - Levant
   * - BEN
     - Benghazi
     - Libya
     - Maghreb
   * - CAI
     - Cairo
     - Egypt
     - Nile Basin
   * - DAM
     - Damascus
     - Syria
     - Levant
   * - DOH
     - Doha
     - Qatar
     - Gulf
   * - FES
     - Fes
     - Morocco
     - Maghreb
   * - JED
     - Jeddah
     - Saudi Arabia
     - Gulf
   * - JER
     - Jerusalem
     - Palestine
     - Levant
   * - KHA
     - Khartoum
     - Sudan
     - Nile Basin
   * - MOS
     - Mosul
     - Iraq
     - Iraq
   * - MSA
     - Modern Standard Arabic
     - Modern Standard Arabic
     - Modern Standard Arabic
   * - MUS
     - Muscat
     - Oman
     - Gulf
   * - RAB
     - Rabat
     - Morocco
     - Maghreb
   * - RIY
     - Riyadh
     - Saudi Arabia
     - Gulf
   * - SAL
     - Salt
     - Jordan
     - Levant
   * - SAN
     - Sana'a
     - Yemen
     - Gulf of Aden
   * - SFX
     - Sfax
     - Tunisia
     - Maghreb
   * - TRI
     - Tripoli
     - Libya
     - Maghreb
   * - TUN
     - Tunis
     - Tunisia
     - Maghreb


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
