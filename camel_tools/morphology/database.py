# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2022 New York University Abu Dhabi
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

"""The database component of CAMeL Tools.
"""

from __future__ import absolute_import

from collections import namedtuple
from pathlib import Path
import re

from camel_tools.utils.stringutils import force_unicode
from camel_tools.morphology.utils import strip_lex
from camel_tools.morphology.errors import InvalidDatabaseFlagError
from camel_tools.morphology.errors import DatabaseParseError
from camel_tools.data import CATALOGUE


MorphologyDBFlags = namedtuple('MorphologyDBFlags', ['analysis', 'generation',
                                                     'reinflection'])


class MorphologyDB:
    """Class providing indexes from a given morphology database file.

    Args:
        fpath (:obj:`str`): File path to database.
        flags (:obj:`str`): Flag string (similar to opening files) indicates
            what components the database will be used for. 'a' indicates
            analysis, 'g' indicates generation, and 'r' indicates indicates
            reinflection. 'r' is equivalent to 'ag' since the reinflector
            uses both analyzer and generator components internally.
            Defaults to 'a'.

    Raises:
        :obj:`~camel_tools.morphology.errors.InvalidDatabaseFlagError`: When
            an invalid flag value is given.
    """

    @staticmethod
    def list_builtin_dbs():
        """Returns a list of builtin databases provided with CAMeL Tools.

        Returns:
            :obj:`list` of :obj:`~camel_tools.data.DatasetEntry`: List of
            builtin databases.
        """

        return list(CATALOGUE.get_component('MorphologyDB').datasets)

    @staticmethod
    def builtin_db(db_name=None, flags='a'):
        """Create a :obj:`MorphologyDB` instance from one of the builtin
        databases provided.

        Args:
            db_name (:obj:`str`, optional): Name of builtin database.
                You can use :meth:`list_builtin_dbs` to get a list of
                builtin databases or see :ref:`camel_morphology_dbs`.
                Defaults to 'calima-msa-r13'.
            flags (:obj:`str`, optional): Flag string to be passed to
                :obj:`MorphologyDB` constructor. Defaults to 'a'.

        Returns:
            :obj:`MorphologyDB`: Instance of builtin database with given flags.
        """

        if db_name is None:
            db_name = CATALOGUE.components['MorphologyDB'].default

        db_info = CATALOGUE.components['MorphologyDB'].datasets[db_name]

        return MorphologyDB(str(Path(db_info.path, 'morphology.db')), flags)

    def __init__(self, fpath, flags='a'):
        """Class constructor.
        """

        self._withAnalysis = False
        self._withReinflection = False
        self._withGeneration = False
        self._defaultKey = 'pos'

        for flag in flags:
            if flag == 'a':
                self._withAnalysis = True
            elif flag == 'g':
                self._withGeneration = True
            elif flag == 'r':
                self._withReinflection = True
                self._withAnalysis = True
                self._withGeneration = True
            else:
                raise InvalidDatabaseFlagError(flag)

        if self._withAnalysis and self._withGeneration:
            self._withReinflection = True

        self.flags = MorphologyDBFlags(self._withAnalysis,
                                       self._withGeneration,
                                       self._withGeneration)
        self.defines = {}
        self.defaults = {}
        self.order = None
        self.tokenizations = set()
        self.compute_feats = frozenset()
        self.stem_backoffs = {}

        self.prefix_hash = {}
        self.suffix_hash = {}
        self.stem_hash = {}

        self.prefix_cat_hash = {}
        self.suffix_cat_hash = {}
        self.lemma_hash = {}

        self.prefix_stem_compat = {}
        self.stem_suffix_compat = {}
        self.prefix_suffix_compat = {}
        self.stem_prefix_compat = {}
        self.max_prefix_size = 0
        self.max_suffix_size = 0

        self._parse_dbfile(fpath)

    def _parse_analysis_line_toks(self, toks):
        res = {}

        for tok in toks:
            if len(tok) == 0:
                continue

            subtoks = tok.split(u':')
            if len(subtoks) < 2:
                raise DatabaseParseError(
                    'invalid key value pair {}'.format(repr(tok)))

            res[subtoks[0]] = u':'.join(subtoks[1:])

        return res

    def _parse_defaults_line_toks(self, toks):
        res = {}

        for tok in toks:
            subtoks = tok.split(u':')
            if len(subtoks) < 2:
                raise DatabaseParseError(
                    'invalid key value pair {} in DEFAULTS'.format(
                        repr(tok)))

            feat = subtoks[0]
            val = ':'.join(subtoks[1:])

            if val == '*':
                res[feat] = None
            else:
                res[feat] = val

        return res

    def _parse_dbfile(self, fpath):
        with open(fpath, 'r', encoding='utf-8') as dbfile:
            # Process DEFINES
            for line in dbfile:
                line = line = force_unicode(line).strip()

                if line == '###DEFINES###':
                    continue

                if line == '###DEFAULTS###':
                    break

                toks = line.split(u' ')

                # Check if line has the minimum viable format
                if len(toks) < 3 or toks[0] != 'DEFINE':
                    raise DatabaseParseError(
                        'invalid DEFINES line {}'.format(repr(line)))

                new_define = toks[1]
                val_set = set()

                # Parse values for defined keyword
                for tok in toks[2:]:
                    subtoks = tok.split(':')

                    # If it's a malformed entry, ignore it
                    if len(subtoks) != 2 and subtoks[0] != toks[1]:
                        raise DatabaseParseError(
                            'invalid key value pair {} in DEFINES'.format(
                                repr(tok)))

                    # If it's an open class, we use None instead of a set
                    if len(toks) == 3 and subtoks[1] == '*open*':
                        val_set = None
                        break

                    val_set.add(subtoks[1])

                self.defines[new_define] = (
                    list(val_set) if val_set is not None else None)

            # Process DEFAULTS
            for line in dbfile:
                line = force_unicode(line).strip()

                if line == '###ORDER###':
                    break

                toks = line.split(u' ')

                if len(toks) < 2 or toks[0] != 'DEFAULT':
                    raise DatabaseParseError(
                        'invalid DEFAULTS line {}'.format(repr(line)))

                parsed_default = self._parse_defaults_line_toks(toks[1:])

                if self._defaultKey not in parsed_default:
                    raise DatabaseParseError(
                        'DEFAULTS line {} missing {} value'.format(
                            repr(line), self._defaultKey))

                dkey = parsed_default[self._defaultKey]
                self.defaults[dkey] = parsed_default

            # Process ORDER
            for line in dbfile:
                line = force_unicode(line).strip()

                if line == '###TOKENIZATIONS###':
                    self.compute_feats = frozenset(self.order)
                    break

                toks = line.split(u' ')

                if (self.order is not None and len(toks) < 2 and
                        toks[0] != 'ORDER'):
                    raise DatabaseParseError(
                        'invalid ORDER line {}'.format(repr(line)))

                if toks[1] not in self.defines:
                    raise DatabaseParseError(
                        'invalid feature {} in ORDER line.'.format(
                            repr(toks[1])))

                self.order = toks[1:]

            # Process TOKENIZATIONS
            for line in dbfile:
                line = force_unicode(line).strip()

                if line == '###STEMBACKOFF###':
                    self.tokenizations = frozenset(self.tokenizations)
                    break

                toks = line.split(u' ')

                if (self.order is not None and len(toks) < 2 and
                        toks[0] != 'TOKENIZATION'):
                    raise DatabaseParseError(
                        'invalid TOKENIZATION line {}'.format(repr(line)))

                if toks[1] not in self.defines:
                    raise DatabaseParseError(
                        'invalid feature {} in TOKENIZATION line.'.format(
                            repr(toks[1])))

                self.tokenizations.update(toks[1:])

            # Process STEMBACKOFFS
            for line in dbfile:
                line = force_unicode(line).strip()

                if line == '###PREFIXES###':
                    break

                toks = line.split(u' ')

                if len(toks) < 3 or toks[0] != 'STEMBACKOFF':
                    raise DatabaseParseError(
                        'invalid STEMBACKOFFS line {}'.format(repr(line)))

                self.stem_backoffs[toks[1]] = toks[2:]

            # Process PREFIXES
            for line in dbfile:
                line = force_unicode(line)
                parts = line.split(u'\t')

                if len(parts) != 3:
                    if line.strip() == '###SUFFIXES###':
                        break
                    raise DatabaseParseError(
                        'invalid PREFIXES line {}'.format(repr(line)))

                prefix = parts[0].strip()
                category = parts[1]
                analysis = self._parse_analysis_line_toks(
                    parts[2].strip().split(u' '))

                if self._withAnalysis:
                    if prefix not in self.prefix_hash:
                        self.prefix_hash[prefix] = []
                    self.prefix_hash[prefix].append((category, analysis))

                if self._withGeneration:
                    # FIXME: Make sure analyses for category are unique?
                    if category not in self.prefix_cat_hash:
                        self.prefix_cat_hash[category] = []
                    self.prefix_cat_hash[category].append(analysis)

            # Process SUFFIXES
            for line in dbfile:
                line = force_unicode(line)
                parts = line.split(u'\t')

                if len(parts) != 3:
                    if line.strip() == '###STEMS###':
                        break
                    raise DatabaseParseError(
                        'invalid SUFFIXES line {}'.format(repr(line)))

                suffix = parts[0].strip()
                category = parts[1]
                analysis = self._parse_analysis_line_toks(
                    parts[2].strip().split(u' '))

                if self._withAnalysis:
                    if suffix not in self.suffix_hash:
                        self.suffix_hash[suffix] = []
                    self.suffix_hash[suffix].append((category, analysis))

                if self._withGeneration:
                    # FIXME: Make sure analyses for category are unique?
                    if category not in self.suffix_cat_hash:
                        self.suffix_cat_hash[category] = []
                    self.suffix_cat_hash[category].append(analysis)

            # Process STEMS
            for line in dbfile:
                line = force_unicode(line).strip()

                if line == '###TABLE AB###':
                    break

                parts = line.split(u'\t')

                if len(parts) != 3:
                    raise DatabaseParseError(
                        'invalid STEMS line {}'.format(repr(line)))

                stem = parts[0]
                category = parts[1]
                analysis = self._parse_analysis_line_toks(parts[2].split(u' '))
                analysis['lex'] = strip_lex(analysis['lex'])

                if self._withAnalysis:
                    if stem not in self.stem_hash:
                        self.stem_hash[stem] = []
                    self.stem_hash[stem].append((category, analysis))

                if self._withGeneration:
                    # FIXME: Make sure analyses for category are unique?
                    lemma_key = analysis['lex']
                    analysis['stemcat'] = category
                    if lemma_key not in self.lemma_hash:
                        self.lemma_hash[lemma_key] = []
                    self.lemma_hash[lemma_key].append(analysis)

            # Process prefix_stem compatibility table
            for line in dbfile:
                line = force_unicode(line).strip()

                if line == '###TABLE BC###':
                    break

                toks = line.split()

                if len(toks) != 2:
                    raise DatabaseParseError(
                        'invalid TABLE AB line {}'.format(repr(line)))

                prefix_cat = toks[0]
                stem_cat = toks[1]

                if self._withAnalysis:
                    if prefix_cat not in self.prefix_stem_compat:
                        self.prefix_stem_compat[prefix_cat] = set()
                    self.prefix_stem_compat[prefix_cat].add(stem_cat)

                if self._withGeneration:
                    if stem_cat not in self.stem_prefix_compat:
                        self.stem_prefix_compat[stem_cat] = set()
                    self.stem_prefix_compat[stem_cat].add(prefix_cat)

            # Process stem_suffix compatibility table
            for line in dbfile:
                line = force_unicode(line).strip()

                if line == '###TABLE AC###':
                    break

                toks = line.split()

                if len(toks) != 2:
                    raise DatabaseParseError(
                        'invalid TABLE BC line {}'.format(repr(line)))

                stem_cat = toks[0]
                suffix_cat = toks[1]

                if stem_cat not in self.stem_suffix_compat:
                    self.stem_suffix_compat[stem_cat] = set()
                self.stem_suffix_compat[stem_cat].add(suffix_cat)

            # Process prefix_suffix compatibility table
            for line in dbfile:
                line = force_unicode(line).strip()

                toks = line.split()

                if len(toks) != 2:
                    raise DatabaseParseError(
                        'invalid TABLE AC line {}'.format(repr(line)))

                prefix_cat = toks[0]
                suffix_cat = toks[1]

                if prefix_cat not in self.prefix_suffix_compat:
                    self.prefix_suffix_compat[prefix_cat] = set()
                self.prefix_suffix_compat[prefix_cat].add(suffix_cat)

            if self._withAnalysis:
                for prefix in self.prefix_hash.keys():
                    self.max_prefix_size = max(self.max_prefix_size,
                                               len(prefix))
                for suffix in self.suffix_hash.keys():
                    self.max_suffix_size = max(self.max_suffix_size,
                                               len(suffix))

    def all_feats(self):
        """Return a set of all features provided by this database instance.

        Returns:
            :obj:`frozenset` of :obj:`str`: The set all features provided by
            this database instance.
        """

        return frozenset(self.defines.keys())

    def tok_feats(self):
        """Return a set of tokenization features provided by this database
        instance.

        Returns:
            :obj:`frozenset` of :obj:`str`: The set tokenization features
            provided by this database instance.
        """

        return self.tokenizations
