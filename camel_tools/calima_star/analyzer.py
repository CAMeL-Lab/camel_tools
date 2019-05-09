# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2019 New York University Abu Dhabi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""The morphological analyzer component of CALIMA Star.
"""


from __future__ import absolute_import

from collections import deque, namedtuple
import copy
import itertools
import re
from threading import RLock

from cachetools import LFUCache, cached

from camel_tools.utils.charsets import UNICODE_PUNCT_SYMBOL_CHARSET
from camel_tools.utils.charsets import AR_CHARSET, AR_DIAC_CHARSET

from camel_tools.utils.charmap import CharMapper
from camel_tools.calima_star.database import CalimaStarDB
from camel_tools.calima_star.errors import AnalyzerError
from camel_tools.calima_star.utils import merge_features
from camel_tools.utils.dediac import dediac_ar


_ALL_PUNC = u''.join(UNICODE_PUNCT_SYMBOL_CHARSET)

_DIAC_RE = re.compile(u'[' + re.escape(u''.join(AR_DIAC_CHARSET)) + u']')
_IS_DIGIT_RE = re.compile(u'^.*[0-9\u0660-\u0669]+.*$')
_IS_STRICT_DIGIT_RE = re.compile(u'^[0-9\u0660-\u0669]+$')
_IS_PUNC_RE = re.compile(u'^[' + re.escape(_ALL_PUNC) + u']+$')
_HAS_PUNC_RE = re.compile(u'[' + re.escape(_ALL_PUNC) + u']')
_IS_AR_RE = re.compile(u'^[' + re.escape(u''.join(AR_CHARSET)) + u']+$')

# Identify No Analysis marker
_NOAN_RE = re.compile(u'NOAN')

DEFAULT_NORMALIZE_MAP = CharMapper({
    u'\u0625': u'\u0627',
    u'\u0623': u'\u0627',
    u'\u0622': u'\u0627',
    u'\u0671': u'\u0627',
    u'\u0649': u'\u064a',
    u'\u0629': u'\u0647',
    u'\u0640': u''
})
""":obj:`~camel_tools.utils.charmap.CharMapper`: The default character map used
for normalization by :obj:`CalimaStarAnalyzer`.

Removes the tatweel/kashida character and does the following conversions:

- 'إ' to 'ا'
- 'أ' to 'ا'
- 'آ' to 'ا'
- 'ٱ' to 'ا'
- 'ى' to 'ي'
- 'ة' to 'ه'
"""


_BACKOFF_TYPES = frozenset(['NONE', 'NOAN_ALL', 'NOAN_PROP', 'ADD_ALL',
                            'ADD_PROP'])


class AnalyzedWord(namedtuple('AnalyzedWord', ['word', 'analyses'])):
    """A named tuple containing a word and its analyses.

    Attributes:
        word (:obj:`str`): The analyzed word.

        analyses (:obj:`list` of :obj:`dict`): List of analyses for **word**.
            See :doc:`/reference/calima_star_features` for more information on
            features and their values.
    """


def _is_digit(word):
    return _IS_DIGIT_RE.match(word) is not None


def _is_strict_digit(word):
    return _IS_STRICT_DIGIT_RE.match(word) is not None


def _is_punc(word):
    return _IS_PUNC_RE.match(word) is not None


def _has_punc(word):
    return _HAS_PUNC_RE.search(word) is not None


def _is_ar(word):
    return _IS_AR_RE.match(word) is not None


def _segments_gen(word, max_prefix=1, max_suffix=1):
    w = len(word)
    for p in range(0, min(max_prefix, w - 1) + 1):
        prefix = word[:p]
        for s in range(max(1, w - p - max_suffix), w - p + 1):
            stem = word[p:p+s]
            suffix = word[p+s:]
            yield (prefix, stem, suffix)


class CalimaStarAnalyzer:
    """CALIMA Star analyzer component.

    Args:
        db (:obj:`~camel_tools.calima_star.database.CalimaStarDB`): Database to
            use for analysis. Must be opened in analysis or reinflection mode.
        backoff (:obj:`str`, optional): Backoff mode. Can be one of the
            following: 'NONE', 'NOAN_ALL', 'NOAN_PROP', 'ADD_ALL', or
            'ADD_PROP'. Defaults to 'NONE'.
        norm_map (:obj:`~camel_tools.utils.charmap.CharMapper`, optional):
            Character map for normalizing input words. Defaults to
            :const:`DEFAULT_NORMALIZE_MAP`.
        strict_digit (:obj:`bool`, optional): If set to `True`, then only words
            completely comprised of digits are considered numbers, otherwise,
            all words containing a digit are considered numbers. Defaults to
            `False`.
        cache_size (:obj:`int`, optional): If greater than zero, then the
            analyzer will cache the analyses for the **cache_Size** most
            frequent words, otherwise no analyses will be cached.

    Raises:
        :obj:`~camel_tools.calima_star.errors.AnalyzerError`: If database is
            not an instance of
            (:obj:`~camel_tools.calima_star.database.CalimaStarDB`), if **db**
            does not support analysis, or if **backoff** is not a valid backoff
            mode.
    """

    def __init__(self, db, backoff='NONE',
                 norm_map=DEFAULT_NORMALIZE_MAP,
                 strict_digit=False,
                 cache_size=0):
        if not isinstance(db, CalimaStarDB):
            raise AnalyzerError('DB is not an instance of CalimaStarDB')
        if not db.flags.analysis:
            raise AnalyzerError('DB does not support analysis')

        self._db = db

        self._backoff = backoff
        self._norm_map = DEFAULT_NORMALIZE_MAP
        self._strict_digit = strict_digit

        if backoff in _BACKOFF_TYPES:
            if backoff == 'NONE':
                self._backoff_condition = None
                self._backoff_action = None
            else:
                backoff_toks = backoff.split('_')
                self._backoff_condition = backoff_toks[0]
                self._backoff_action = backoff_toks[1]
        else:
            raise AnalyzerError('Invalid backoff mode {}'.format(
                repr(backoff)))

        if isinstance(cache_size, int):
            if cache_size > 0:
                cache = LFUCache(cache_size)
                self.analyze = cached(cache, lock=RLock())(self.analyze)

        else:
            raise AnalyzerError('Invalid cache size {}'.format(
                                repr(cache_size)))

    def _normalize(self, word):
        if self._norm_map is None:
            return word
        return self._norm_map.map_string(word)

    def _combined_analyses(self,
                           word_dediac,
                           prefix_analyses,
                           stem_analyses,
                           suffix_analyses):
        combined = deque()

        for p in itertools.product(prefix_analyses, stem_analyses):
            prefix_cat = p[0][0]
            prefix_feats = p[0][1]
            stem_cat = p[1][0]
            stem_feats = p[1][1]

            if stem_cat in self._db.prefix_stem_compat[prefix_cat]:
                for suffix_cat, suffix_feats in suffix_analyses:
                    if ((stem_cat not in self._db.stem_suffix_compat) or
                        (prefix_cat not in self._db.prefix_suffix_compat) or
                        (suffix_cat not in
                         self._db.stem_suffix_compat[stem_cat]) or
                        (suffix_cat not in
                         self._db.prefix_suffix_compat[prefix_cat])):
                        continue

                    merged = merge_features(self._db, prefix_feats, stem_feats,
                                            suffix_feats)
                    merged['stem'] = stem_feats['diac']
                    merged['stemcat'] = stem_cat

                    merged_dediac = dediac_ar(merged['diac'])
                    if word_dediac != merged_dediac:
                        merged['source'] = 'spvar'

                    combined.append(merged)

        return combined

    def _combined_backoff_analyses(self,
                                   stem,
                                   word_dediac,
                                   prefix_analyses,
                                   stem_analyses,
                                   suffix_analyses):
        combined = deque()

        for p in itertools.product(prefix_analyses, stem_analyses):
            prefix_cat = p[0][0]
            prefix_feats = p[0][1]
            stem_cat = p[1][0]
            stem_feats = copy.copy(p[1][1])

            if stem_cat in self._db.prefix_stem_compat[prefix_cat]:
                for suffix_cat, suffix_feats in suffix_analyses:
                    if ((suffix_cat not in
                         self._db.stem_suffix_compat[stem_cat]) or
                        (prefix_cat not in self._db.prefix_suffix_compat or
                         suffix_cat not in
                         self._db.prefix_suffix_compat[prefix_cat])):
                        continue

                    if (self._backoff_action == 'PROP' and
                            'NOUN_PROP' not in stem_feats['bw']):
                        continue

                    stem_feats['bw'] = _NOAN_RE.sub(stem, stem_feats['bw'])
                    stem_feats['diac'] = _NOAN_RE.sub(stem, stem_feats['diac'])
                    stem_feats['lex'] = _NOAN_RE.sub(stem, stem_feats['lex'])

                    merged = merge_features(self._db, prefix_feats, stem_feats,
                                            suffix_feats)

                    merged['stem'] = stem_feats['diac']
                    merged['stemcat'] = stem_cat
                    merged['source'] = 'backoff'
                    merged['gloss'] = stem_feats['gloss']

                    combined.append(merged)

        return combined

    def analyze(self, word):
        """Analyze a given word.

        Args:
            word (:py:obj:`str`): Word to analyze.

        Returns:
            :obj:`list` of :obj:`dict`: The list of analyses for **word**.
            See :doc:`/reference/calima_star_features` for more information on
            features and their values.
        """

        word = word.strip()

        if word == '':
            return []

        analyses = deque()
        word_dediac = dediac_ar(word)
        word_normal = self._normalize(word_dediac)

        if ((self._strict_digit and _is_strict_digit(word)) or
                (not self._strict_digit and _is_digit(word))):
            result = copy.copy(self._db.defaults['digit'])
            result['diac'] = word
            result['lex'] = word + '_0'
            result['bw'] = word + '/NOUN_NUM'
            result['gloss'] = word
            result['source'] = 'digit'
            analyses.append(result)
        elif _is_punc(word):
            result = copy.copy(self._db.defaults['punc'])
            result['diac'] = word
            result['lex'] = word + '_0'
            result['bw'] = word + '/PUNC'
            result['gloss'] = word
            result['source'] = 'punc'
            analyses.append(result)
        elif _has_punc(word):
            pass
        elif not _is_ar(word):
            result = copy.copy(self._db.defaults['noun'])
            result['diac'] = word
            result['lex'] = word + '_0'
            result['bw'] = word + '/FOREIGN'
            result['gloss'] = word
            result['source'] = 'foreign'
            analyses.append(result)
        else:
            segments_gen = _segments_gen(word_normal, self._db.max_prefix_size,
                                         self._db.max_suffix_size)

            for segmentation in segments_gen:
                prefix = segmentation[0]
                stem = segmentation[1]
                suffix = segmentation[2]

                prefix_analyses = self._db.prefix_hash.get(prefix, None)
                suffix_analyses = self._db.suffix_hash.get(suffix, None)

                if prefix_analyses is None or suffix_analyses is None:
                    continue

                stem_analyses = self._db.stem_hash.get(stem, None)

                if stem_analyses is not None:
                    combined = self._combined_analyses(word_dediac,
                                                       prefix_analyses,
                                                       stem_analyses,
                                                       suffix_analyses)
                    analyses.extend(combined)

        if ((self._backoff_condition == 'NOAN' and len(analyses) == 0) or
                (self._backoff_condition == 'ADD')):

            segments_gen = _segments_gen(word_normal,
                                         self._db.max_prefix_size,
                                         self._db.max_suffix_size)

            backoff_cats = self._db.stem_backoffs[self._backoff_action]
            stem_analyses = [(cat, analysis)
                             for cat, analysis in self._db.stem_hash['NOAN']
                             if cat in backoff_cats]

            for segmentation in segments_gen:
                prefix = segmentation[0]
                stem = segmentation[1]
                suffix = segmentation[2]

                prefix_analyses = self._db.prefix_hash.get(prefix, None)
                suffix_analyses = self._db.suffix_hash.get(suffix, None)

                if prefix_analyses is None or suffix_analyses is None:
                    continue

                combined = self._combined_backoff_analyses(stem,
                                                           word_dediac,
                                                           prefix_analyses,
                                                           stem_analyses,
                                                           suffix_analyses)
                analyses.extend(combined)

        result = list(analyses)

        return result

    def analyze_words(self, words):
        '''Analyze a list of words.

        Args:
            words (:py:obj:`list` of :py:obj:`str`): List of words to analyze.

        Returns:
            :obj:`list` of :obj:`AnalyzedWord`: The list of analyses for each
            word in **words**.
        '''

        return list(map(lambda w: AnalyzedWord(w, self.analyze(w)), words))
