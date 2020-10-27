camel_tools.tagger.default
==========================

.. automodule:: camel_tools.tagger.default


Classes
-------

.. autoclass:: camel_tools.tagger.default.DefaultTaggerError
   :members:

.. autoclass:: camel_tools.tagger.default.InvalidDefaultTaggerDisambiguator
   :members:

.. autoclass:: camel_tools.tagger.default.InvalidDefaultTaggerFeature
   :members:

.. autoclass:: camel_tools.tagger.default.DefaultTagger
   :members:

Features
--------

The list of features that can be produced by :obj:`DefaultTagger` are:
:code:`'diac'`, :code:`'bw'`, :code:`'asp'`, :code:`'cas'`, :code:`'gen'`,
:code:`'mod'`, :code:`'num'`, :code:`'per'`, :code:`'pos'`, :code:`'enc0'`,
:code:`'enc1'`, :code:`'enc2'`, :code:`'prc0'`, :code:`'prc1'`, :code:`'prc2'`,
:code:`'prc3'`, :code:`'form_num'`, :code:`'form_gen'`, :code:`'stt'`,
:code:`'vox'`, :code:`'atbtok'`, :code:`'atbseg'`, :code:`bwtok`,
:code:`'d1tok'`, :code:`'d1seg'`, :code:`'d2tok'`, :code:`'d2seg'`,
:code:`'d3tok'`, :code:`'d3seg'`, :code:`'catib6'`, :code:`'ud'`,
:code:`'caphi'`.

See See :doc:`/reference/camel_morphology_features` for more information on
features and their values.


Examples
--------

.. code-block:: python

   from camel_tools.disambig.mle import MLEDisambiguator
   from camel_tools.tagger.default import DefaultTagger

   mled = MLEDisambiguator.pretrained()
   tagger = DefaultTagger(mled, 'pos')

   tagger.tag('ذهبت الى المدرسة'.split())
