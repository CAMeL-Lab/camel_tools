camel_tools.tokenizers.morphological
====================================

.. automodule:: camel_tools.tokenizers.morphological

Classes
-------

.. autoclass:: camel_tools.tokenizers.morphological.MorphologicalTokenizer
   :members:

Examples
--------

.. code-block:: python

   from camel_tools.disambig.mle import MLEDisambiguator
   from camel_tools.tokenizers.morphological import MorphologicalTokenizer

   # Initialize disambiguators
   mle_msa = MLEDisambiguator.pretrained('calima-msa-r13')
   mle_egy = MLEDisambiguator.pretrained('calima-egy-r13')

   # We expect a sentence to be whitespace/punctuation tokenized beforehand.
   # We provide a simple whitespace and punctuation tokenizer as part of camel_tools.
   # See camel_tools.tokenizers.word.simple_word_tokenize.
   sentence_msa = ['فتنفست', 'الصعداء']
   sentence_egy = ['وكاتباله', 'مكتوبين']

   # Create different morphological tokenizer instances
   msa_d3_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='d3tok')
   msa_atb_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='atbtok')
   msa_bw_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='bwtok')
   egy_bw_tokenizer = MorphologicalTokenizer(disambiguator=mle_egy, scheme='bwtok')

   # Generate tokenizations
   # Note that our Egyptian resources currently provide bwtok tokenization only. 
   msa_d3_tok = msa_d3_tokenizer.tokenize(sentence_msa)
   msa_atb_tok = msa_atb_tokenizer.tokenize(sentence_msa)
   msa_bw_tok = msa_bw_tokenizer.tokenize(sentence_msa)
   egy_bw_tok = egy_bw_tokenizer.tokenize(sentence_egy)

   # Print results
   print('D3 tokenization (MSA):', msa_d3_tok)
   print('ATB tokenization (MSA):', msa_atb_tok)
   print('BW tokenization (MSA):', msa_bw_tok)
   print('BW tokenization (EGY):', egy_bw_tok)

This will output:

.. code-block:: none

   D3 tokenization (MSA): ['ف+_تنفست', 'ال+_صعداء']
   ATB tokenization (MSA): ['ف+_تنفست', 'الصعداء']
   BW tokenization (MSA): ['ف+_تنفس_+ت', 'ال+_صعداء']
   BW tokenization (EGY): ['و+_كاتب_+ة_+ل_+ه', 'مكتوب_+ين']