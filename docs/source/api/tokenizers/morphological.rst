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
   d3_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='d3tok', split=True)
   atb_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='atbtok', diac=True)
   bw_tokenizer = MorphologicalTokenizer(disambiguator=mle_egy, scheme='bwtok')

   # Generate tokenizations
   # Note that our Egyptian resources currently provide bwtok tokenization only. 
   d3_tok = d3_tokenizer.tokenize(sentence_msa)
   atb_tok = atb_tokenizer.tokenize(sentence_msa)
   bw_tok = bw_tokenizer.tokenize(sentence_egy)

   # Print results
   print('D3 tokenization: ', d3_tok)
   print('ATB tokenization: ', atb_tok)
   print('BW tokenization: ', bw_tok)

This will output:

.. code-block:: none

   D3 tokenization:  ['ف+', 'تنفست', 'ال+', 'صعداء']
   ATB tokenization:  ['فَ+_تَنَفَّسْتُ', 'الصُّعَداءَ']
   BW tokenization:  ['و+_كاتب_+ة_+ل_+ه', 'مكتوب_+ين']