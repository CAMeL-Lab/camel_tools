CAMeL Morphology Features
=========================

Below is a listing of all the features and their respective values produced or
required by the morphological analyzer, generator, and reinflector.

Morphological Features
^^^^^^^^^^^^^^^^^^^^^^

The following features provide morphological information in a given analysis.
All these features have a closed set of possible values as described below.

* **asp** - Aspect

  * **c** - Command
  * **i** - Imperfective
  * **p** - Perfective
  * **na** - Not applicable

* **cas** - Case

  * **n** - Nominative
  * **a** - Accusative
  * **g** - Genitive
  * **na** - Not applicable
  * **u** - Undefined

* **form_gen** - Form gender

  * **f** - Feminine
  * **m** - Masculine
  * **na** - Not applicable

* **form_num** - Form number

  * **s** - Singular
  * **d** - Dual
  * **p** - Plural
  * **na** - Not applicable
  * **u** - Undefined

* **gen** - Gender

  * **f** - Feminine
  * **m** - Masculine
  * **na** - Not applicable

* **mod** - Mood

  * **i** - Indicative
  * **j** - Jussive
  * **s** - Subjunctive
  * **na** - Not applicable
  * **u** - Undefined

* **num** - Number

  * **s** - Singular
  * **d** - Dual
  * **p** - Plural
  * **na** - Not applicable
  * **u** - Undefined

* **per** - Person

  * **1** - 1st
  * **2** - 2nd
  * **3** - 3rd
  * **na** - Not applicable

* **rat** - Rationality

  * **n** - No (irrational)
  * **y** - Yes (rational)
  * **na** - Not applicable

* **stt** - State

  * **c** - Construct/Poss/Idafa
  * **d** - Definite
  * **i** - Indefinite
  * **na** - Not applicable
  * **u** - Undefined

* **vox** - Voice

  * **a** - Active
  * **p** - Passive
  * **na** - Not applicable
  * **u** - Undefined

* **pos** - Part-of-speech

  * **noun** - Noun
  * **noun_prop** - Proper noun
  * **noun_num** - Number noun
  * **noun_quant** - Quantity noun
  * **adj** - Adjective
  * **adj_comp** - Comparitive adjective
  * **adj_num** - Numerical adjective
  * **adv** - Adverb
  * **adv_interrog** - Interrogative adverb
  * **adv_rel** - Relative adverb
  * **pron** - Pronoun
  * **pron_dem** - Demonstrative pronoun
  * **pron_exclam** - Pronoun exclamation
  * **pron_interrog** - Interrogative pronoun
  * **pron_rel** - Relative pronoun
  * **verb** - Verb
  * **verb_pseudo** - Pseudo verb
  * **part** - Particle
  * **part_dem** - Demonstrative particle
  * **part_det** - Determiner particle
  * **part_focus** - Focus particle
  * **part_fut** - Future marker particle
  * **part_interrog** - Interrogative particle
  * **part_neg** - Negative particle
  * **part_restrict** - Restricitve particle
  * **part_verb** - Verbal particle
  * **part_voc** - Vocalized particle
  * **prep** - Preposition
  * **abbrev** - Abbreviation
  * **punc** - Punctuation
  * **conj** - Conjunction
  * **conj_sub** - Subordinating conjunction
  * **interj** - Interjection
  * **digit** - Digital numbers
  * **latin** - Latin/foreign

* **prc0** - Article proclitic

  * **0** - No proclitic
  * **na** - Not applicable
  * **Aa_prondem** - Demonstrative particle *Aa*
  * **Al_det** - Determiner
  * **AlmA_neg** - Determiner *Al* + negative particle *mA*
  * **lA_neg** - Negative particle *lA*
  * **mA_neg** - Negative particle *mA*
  * **ma_neg** - Negative particle *ma*
  * **mA_part** - Particle *mA*
  * **mA_rel** - Relative pronoun *mA*

* **prc1** - Preposition proclitic

  * **0** - No proclitic
  * **na** - Not applicable
  * **<i$_interrog** - Interrogative *ish*
  * **bi_part** - Particle *bi*
  * **bi_prep** - Preposition *bi*
  * **bi_prog** - Progressive verb particle *bi*
  * **Ea_prep** - Preposition *Ea*
  * **EalaY_prep** - Preposition *EalaY*
  * **fiy_prep** - Preposition *fy*
  * **hA_dem** - Demonstrative *hA*
  * **Ha_fut** - Future marker *Ha*
  * **ka_prep** - Preposition *ka*
  * **la_emph** - Emphatic particle *la*
  * **la_prep** - Preposition *la*
  * **la_rc** - Response conditional *la*
  * **libi_prep** - Preposition *li* + preposition *bi*
  * **laHa_emphfut** - Emphatic *la* + future marker *Ha*
  * **laHa_rcfut** - Response conditional *la* + future marker *Ha*
  * **li_jus** - Jussive *li*
  * **li_sub** - Subjunctive *li*
  * **li_prep** - Preposition *li*
  * **min_prep** - Preposition *min*
  * **sa_fut** - Future marker *sa*
  * **ta_prep** - Preposition *ta*
  * **wa_part** - Particle *wa*
  * **wa_prep** - Preposition *wa*
  * **wA_voc** - Vocative *wA*
  * **yA_voc** - Vocative *yA*

* **prc2** - Conjunction proclitic

  * **0** - No proclitic
  * **na** - Not applicable
  * **fa_conj** - Conjunction *fa*
  * **fa_conn** - Connective particle *fa*
  * **fa_rc** - Responsive conditional *fa*
  * **fa_sub** - Subordinating conjunction *fa*
  * **wa_conj** - conjunction *wa*
  * **wa_part** - particle *wa*
  * **wa_sub** - Subordinating conjunction *wa*

* **prc3** - Question proclitic

  * **0** - No proclitic
  * **na** - Not applicable
  * **>a_ques** - Interrogative partical *>a*

* **enc0** - Pronominal enclitic

  * **0** - No enclitic
  * **na** - Not spplicable
  * **1s_dobj** - 1st person singular direct object
  * **1s_poss** - 1st person singular possessive
  * **1s_pron** - 1st person singular pronoun
  * **1p_dobj** - 1st person plural direct object
  * **1p_poss** - 1st person plural possessive
  * **1p_pron** - 1st person plural pronoun
  * **2d_dobj** - 2nd person dual direct object
  * **2d_poss** - 2nd person dual possessive
  * **2d_pron** - 2nd person dual pronoun
  * **2p_dobj** - 2nd person plural direct object
  * **2p_poss** - 2nd person plural possessive
  * **2p_pron** - 2nd person plural pronoun
  * **2fs_dobj** - 2nd person feminine singular direct object
  * **2fs_poss** - 2nd person feminine singular possessive
  * **2fs_pron** - 2nd person feminine singular pronoun
  * **2fp_dobj** - 2nd person feminine plural direct object
  * **2fp_poss** - 2nd person feminine plural possessive
  * **2fp_pron** - 2nd person feminine plural pronoun
  * **2ms_dobj** - 2nd person masculine singular direct object
  * **2ms_poss** - 2nd person masculine singular possessive
  * **2ms_pron** - 2nd person masculine singular pronoun
  * **2mp_dobj** - 2nd person masculine plural direct object
  * **2mp_poss** - 2nd person masculine plural possessive
  * **2mp_pron** - 2nd person masculine plural pronoun
  * **3d_dobj** - 3rd person dual direct object
  * **3d_poss** - 3rd person dual possessive
  * **3d_pron** - 3rd person dual pronoun
  * **3p_dobj** - 3rd person plural direct object
  * **3p_poss** - 3rd person plural possessive
  * **3p_pron** - 3rd person plural pronoun
  * **3fs_dobj** - 3rd person feminine singular direct object
  * **3fs_poss** - 3rd person feminine singular possessive
  * **3fs_pron** - 3rd person feminine singular pronoun
  * **3fp_dobj** - 3rd person feminine plural direct object
  * **3fp_poss** - 3rd person feminine plural possessive
  * **3fp_pron** - 3rd person feminine plural pronoun
  * **3ms_dobj** - 3rd person masculine singular direct object
  * **3ms_poss** - 3rd person masculine singular possessive
  * **3ms_pron** - 3rd person masculine singular pronoun
  * **3mp_dobj** - 3rd person masculine plural direct object
  * **3mp_poss** - 3rd person masculine plural possessive
  * **3mp_pron** - 3rd person masculine plural pronoun
  * **Ah_voc** - Vocative particle *Ah*
  * **lA_neg** - Negative particle *lA*
  * **ma_interrog** - Interrogative pronoun *ma*
  * **mA_interrog** - Interrogative pronoun *mA*
  * **man_interrog** - Interrogative pronoun *man*
  * **ma_rel** - Relative pronoun *ma*
  * **mA_rel** - Relative pronoun *mA*
  * **man_rel** - Relative pronoun *man*
  * **ma_sub** - Subordinating conjunction *ma*
  * **mA_sub** - Subordinating conjunction *mA*

Lexical Features
^^^^^^^^^^^^^^^^

* **diac** - Diacritized word
* **lex** - Lemma
* **root** - Traditional Arabic root consonants
* **atbtok** - ATB tokenization
* **d3tok** - D3 tokenization
* **bwtok** - Buckwalter POS tag based tokenization

.. * **atbseg** - ATB segmentation
.. * **d1tok** - D1 tokenization
.. * **d1seg** - D1 segmentation
.. * **d2tok** - D2 tokenization
.. * **d2seg** - D2 segmentation
.. * **d3seg** - D3 segmentation

Other Features
^^^^^^^^^^^^^^

* **bw** - Buckwalter POS tag

* **caphi** - CAPHI phonological representation

  * **None** - No CAPHI representation
  * CAPHI phonological representation using underscore as a seperatore (instead
    of white space).
    `See here <https://sites.google.com/a/nyu.edu/coda/phonology-reference>`_ for
    more information.

* **catib6** - CATiB6 POS tag (consistent with **atbtok**).

* **gloss** - Concatinated English gloss

  * Semicolon seperated glosses of a word if it is in the lexicon.
  * The word itself if a word is foreign, punctuation, or a digit.

* **pattern** - Templatic pattern

  * **None** - No templatic pattern

* **source** - Source of generated analysis

  * **lex** - Lexicon
  * **punct** - Punctuation
  * **foreign** - Foreign word
  * **spvar** - Spelling variant
  * **digit** - Digital number
  * **backoff** - Backoff analysis

* **ud** - Universal Dependencies POS tag (consistent with **atbtok**).

* **pos_logprob** - POS log probability

  * **None** - No log probability
  * The log (base 10) of the probability of the associated **pos** value
    in the database.

* **lex_logprob** - Lemma log probability

  * **None** - No log probability
  * The log (base 10) of the probability of the associated **lex** value
    in the database.

* **pos_lex_logprob** - POS-lemma log probability

  * **None** - No log probability
  * The log (base 10) of the probability of the associated
    **pos**\ -\ **lex** pair values in the database.
