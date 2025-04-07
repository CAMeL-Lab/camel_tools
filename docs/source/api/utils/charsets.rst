camel_tools.utils.charsets
==========================

This module provides a comprehensive list of character sets useful for Arabic text processing.
All character sets are implemented as Python
`frozensets <https://docs.python.org/3.9/library/stdtypes.html#frozenset>`_
and therefore support all frozenset operations.


.. autodata:: camel_tools.utils.charsets.UNICODE_PUNCT_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.UNICODE_SYMBOL_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.UNICODE_LETTER_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.UNICODE_MARK_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.UNICODE_NUMBER_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.UNICODE_PUNCT_SYMBOL_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.UNICODE_LETTER_MARK_NUMBER_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.EMOJI_ALL_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.EMOJI_SINGLECHAR_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.EMOJI_MULTICHAR_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.AR_LETTERS_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.AR_DIAC_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.AR_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.BW_LETTERS_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.BW_DIAC_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.BW_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.SAFEBW_LETTERS_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.SAFEBW_DIAC_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.SAFEBW_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.XMLBW_LETTERS_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.XMLBW_DIAC_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.XMLBW_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.HSB_LETTERS_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.HSB_DIAC_CHARSET
   :no-value:

.. autodata:: camel_tools.utils.charsets.HSB_CHARSET
   :no-value:


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
