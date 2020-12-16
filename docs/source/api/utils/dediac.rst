camel_tools.utils.dediac
========================

This submodule contains functions for dediacritizing Arabic text in different
encodings. See :doc:`/reference/encoding_schemes` for more information on
encodings.

Functions
---------

.. autofunction:: camel_tools.utils.dediac.dediac_ar

.. autofunction:: camel_tools.utils.dediac.dediac_bw

.. autofunction:: camel_tools.utils.dediac.dediac_safebw

.. autofunction:: camel_tools.utils.dediac.dediac_xmlbw

.. autofunction:: camel_tools.utils.dediac.dediac_hsb

Examples
--------

.. code-block:: python

    from camel_tools.utils.dediac import dediac_ar, dediac_bw

    # Strings to dediacritize
    sentence_ar = 'ثابِتُ الدّائِرَةِ هُوَ نِسبَةُ مُحِيطِها لِقُطرِها وَيُعرَفُ بِالثّابِتِ ط'
    sentence_bw = 'vAbitu Ald~A}irapi huwa nisbapu muHiyTihA liquTrihA wayuErafu biAlv~Abiti T'

    # Dediacritize
    sentence_ar_dediac = dediac_ar(sentence_ar)
    sentence_bw_dediac = dediac_bw(sentence_bw)

    # Print results
    print('Diacritized and dediacritized Arabic sentences:\n\t{}\n\t{}'.format(sentence_ar, sentence_ar_dediac))
    print('Diacritized and dediacritized Buckwalter sentences:\n\t{}\n\t{}'.format(sentence_bw, sentence_bw_dediac))

This will output:

.. code-block:: none

    Diacritized and dediacritized Arabic sentences:
            ثابِتُ الدّائِرَةِ هُوَ نِسبَةُ مُحِيطِها لِقُطرِها وَيُعرَفُ بِالثّابِتِ ط
            ثابت الدائرة هو نسبة محيطها لقطرها ويعرف بالثابت ط
    Diacritized and dediacritized Buckwalter sentences:
            vAbitu Ald~A}irapi huwa nisbapu muHiyTihA liquTrihA wayuErafu biAlv~Abiti T
            vAbt AldA}rp hw nsbp mHyThA lqTrhA wyErf bAlvAbt T