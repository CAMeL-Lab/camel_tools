camel_tools.utils.charsets
==========================

This module provides a comprehensive list of character sets useful for Arabic
text processing.

The character sets available in this module are:


* :obj:`UNICODE_PUNCT_CHARSET` - A set of all Unicode characters marked as
  punctuation.
* :obj:`UNICODE_SYMBOL_CHARSET` - A set of all Unicode characters marked as
  symbols.
* :obj:`UNICODE_PUNCT_SYMBOL_CHARSET` - A set of all Unicode characters marked as
  either punctuation or symbol.
* :obj:`EMOJI_SINGLECHAR_CHARSET` - A set of all single-character emojis.
* :obj:`EMOJI_MULTICHAR_CHARSET` - A set of all multi-character emojis.
* :obj:`EMOJI_ALL_CHARSET` - A set of all emojis (union of 
  :obj:`EMOJI_SINGLECHAR_CHARSET` and :obj:`EMOJI_MULTICHAR_CHARSET`).
* :obj:`AR_CHARSET` - A set of all Unicode Arabic letters and diacritics.
* :obj:`AR_LETTERS_CHARSET` - A set of all Unicode Arabic letters.
* :obj:`AR_DIAC_CHARSET` - A set of all Unicode Arabic diacritics.
* :obj:`BW_CHARSET` - A set of all Arabic letters and diacritics in Buckwalter
  encoding.
* :obj:`BW_LETTERS_CHARSET` - A set of all Arabic letters in Buckwalter
  encoding.
* :obj:`BW_DIAC_CHARSET` - A set of all Arabic diacritics in Buckwalter
  encoding.
* :obj:`SAFEBW_CHARSET` - A set of all Arabic letters and diacritics in Safe
  Buckwalter encoding.
* :obj:`SAFEBW_LETTERS_CHARSET` - A set of all Arabic letters in Safe
  Buckwalter encoding.
* :obj:`SAFEBW_DIAC_CHARSET` - A set of all Arabic diacritics in Safe Buckwalter
  encoding.
* :obj:`XMLBW_CHARSET` - A set of all Arabic letters and diacritics in XML
  Buckwalter encoding.
* :obj:`XMLBW_LETTERS_CHARSET` - A set of all Arabic letters in XML Buckwalter
  encoding.
* :obj:`XMLBW_DIAC_CHARSET` - A set of all Arabic diacritics in XML Buckwalter
  encoding.
* :obj:`HSB_CHARSET` - A set of all Arabic letters and diacritics in
  Habash-Soudi-Buckwalter encoding.
* :obj:`HSB_LETTERS_CHARSET` - A set of all Arabic letters in
  Habash-Soudi-Buckwalter encoding.
* :obj:`HSB_DIAC_CHARSET` - A set of all Arabic diacritics in
  Habash-Soudi-Buckwalter encoding.

All character sets are implemented as Python
`frozensets <https://docs.python.org/3.6/library/stdtypes.html#frozenset>`_
and therefore support all frozenset operations.

Using Character Sets
--------------------

The simplest use case for character sets is checking whether a given character
belongs in that set. For example, if we wanted to check if a given character
is an Arabic letter, we can do the following:

.. code-block:: python

   from camel_tools.utils.charsets import AR_LETTERS_CHARSET

   print('A' in AR_LETTERS_CHARSET)
   # False

   print('أ' in AR_LETTERS_CHARSET)
   # True

If we wanted to check whether an entire word is an Arabic word we can use
character sets to build a regular expression as follows:

.. code-block:: python

   import re

   from camel_tools.utils.charsets import AR_CHARSET

   # Concatinate all Arabic characters into a string
   ar_str = u''.join(AR_CHARSET)

   # Compile a regular expression using above string
   arabic_re = re.compile(r'^[' + re.escape(ar_str) + r']+$')

   print(arabic_re.match(u'Arabic') is not None)
   # False

   print(arabic_re.match(u'عربي') is not None)
   # True
