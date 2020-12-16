camel_tools.transliterate
=========================

Contains the Transliterator class for transliterating text using a
:obj:`~camel_tools.utils.charmap.CharMapper`.

Classes
-------

.. autoclass:: camel_tools.utils.transliterate.Transliterator
   :members:

Examples
--------

.. code-block:: python

   from camel_tools.utils.charmap import CharMapper
   from camel_tools.utils.transliterate import Transliterator

   # Instantiate the builtin bw2ar (Buckwalter to Arabic) CharMapper
   bw2ar = CharMapper.builtin_mapper('bw2ar')

   # Instantiate Transliterator with the bw2ar CharMapper with '@@IGNORE@@' marker (default)
   bw2ar_translit = Transliterator(bw2ar)

   # String to transliterate
   sentence_bw = 'Al>um~u madrasapN <i*A >aEdadtahA >aEdadta $aEbAF Tay~iba Al>aErAqi @@IGNORE@@#womenInSTEM'

   # Generate Arabic transliteration from BW
   sentence_ar = bw2ar_translit.transliterate(sentence_bw)

   # Generate Arabic transliteration from BW and strip @@IGNORE@@ marker
   sentence_ar_stripped = bw2ar_translit.transliterate(sentence_ar, strip_markers=True)

   # Print results
   print('Original sentence:\n\t', sentence_bw)
   print('Buckwalter encoded sentence:\n\t', sentence_ar)
   print('Buckwalter encoded sentence + stripped markers:\n\t', sentence_ar_stripped)

This will output:

.. code-block:: none

   Original sentence:
            Al>um~u madrasapN <i*A >aEdadtahA >aEdadta $aEbAF Tay~iba Al>aErAqi @@IGNORE@@#womenInSTEM
   Buckwalter encoded sentence:
            الأُمُّ مَدرَسَةٌ إِذا أَعدَدتَها أَعدَدتَ شَعباً طَيِّبَ الأَعراقِ @@IGNORE@@#womenInSTEM
   Buckwalter encoded sentence + stripped markers:
            الأُمُّ مَدرَسَةٌ إِذا أَعدَدتَها أَعدَدتَ شَعباً طَيِّبَ الأَعراقِ #womenInSTEM