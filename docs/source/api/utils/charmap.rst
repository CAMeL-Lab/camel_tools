camel_tools.utils.charmap
=========================

Contains the :obj:`CharMapper` class for mapping characters in a Unicode string
to other strings.

Classes
-------

.. autoclass:: camel_tools.utils.charmap.CharMapper
   :members:
   :special-members: __call__

.. autoclass:: camel_tools.utils.charmap.InvalidCharMapKeyError

.. autoclass:: camel_tools.utils.charmap.BuiltinCharMapNotFoundError

JSON File Structure
-------------------

JSON files to be used with :obj:`CharMapper` should have the following format:

.. code-block:: json

   {
       "default": "",

       "charMap": {
           "a": "z",
           "b-g": "",
           "x-z": null
       }
   }

The root object in the file should be a dictionary with two keys: 'default' and
'charMap'. These correspond to and follow the same restrictions as the
respective input parameters to the :obj:`CharMapper` constructor (with
`null` in the JSON file corresponding to `None` in Python).


Built-in mappings
-----------------

Below is a listing of built-in mappings:

Arabic Transliteration
^^^^^^^^^^^^^^^^^^^^^^

- **ar2bw** Transliterates Arabic text to Buckwalter scheme.

- **ar2safebw** Transliterates Arabic text to Safe Buckwalter scheme.

- **ar2xmlbw** Transliterates Arabic text to XML Buckwalter scheme.

- **ar2hsb** Transliterates Arabic text to  Habash-Soudi-Buckwalter scheme.

- **bw2ar** Transliterates Buckwalter scheme text to Arabic.

- **bw2safebw** Transliterates Buckwalter scheme text to Safe Buckwalter scheme.

- **bw2xmlbw** Transliterates Buckwalter scheme text to XML Buckwalter scheme.

- **bw2hsb** Transliterates Buckwalter scheme text to Habash-Soudi-Buckwalter
  scheme.

- **safebw2ar** Transliterates Safe Buckwalter scheme text to Arabic.

- **safebw2bw** Transliterates Safe Buckwalter scheme text to Buckwalter scheme.

- **safebw2xmlbw** Transliterates Safe Buckwalter scheme text to XML Buckwalter
  scheme.

- **safebw2hsb** Transliterates Safe Buckwalter scheme text to
  Habash-Soudi-Buckwalter scheme.

- **xmlbw2ar** Transliterates XML Buckwalter Scheme text to Arabic.

- **xmlbw2bw** Transliterates XML Buckwalter Scheme text to Buckwalter scheme.

- **xmlbw2safebw** Transliterates XML Buckwalter Scheme text to Safe Buckwalter
  scheme.

- **xmlbw2hsb** Transliterates XML Buckwalter Scheme text to
  Habash-Soudi-Buckwalter scheme.

- **hsb2ar** Transliterates Habash-Soudi-Buckwalter scheme text to Arabic.

- **hsb2bw** Transliterates Habash-Soudi-Buckwalter scheme text to Buckwalter
  scheme.

- **hsb2safebw** Transliterates Habash-Soudi-Buckwalter scheme text to
  Safe Buckwalter scheme.

- **hsb2xmlbw** Transliterates Habash-Soudi-Buckwalter scheme text to
  XML Buckwalter scheme.


See :doc:`../../reference/encoding_schemes` for more information on Arabic
encoding schemes.

Utility
^^^^^^^

- **arclean** Cleans Arabic text by

    - Deleting characters that are not in Arabic, ASCII, or Latin-1.
    - Converting all spacing characters to an ASCII space character.
    - Converting Indic digits into Arabic digits.
    - Converting extended Arabic letters into basic Arabic letters.
    - Converting 1-char presentation froms into simple basic forms.
