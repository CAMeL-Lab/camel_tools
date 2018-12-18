# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018 New York University Abu Dhabi
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

"""The database component of CALIMA Star.
"""

from __future__ import absolute_import

from collections import namedtuple
import os.path
import re

from camel_tools.utils.stringutils import force_unicode
from camel_tools.calima_star.errors import InvalidDatabaseFlagError
from camel_tools.calima_star.errors import InvalidBuiltinDatabaseName
from camel_tools.calima_star.errors import DatabaseParseError

DBListing = namedtuple('DBListing', ['name', 'version'])

_DATABASES_DIR = os.path.join(os.path.dirname(__file__), 'databases')
_DATABASES = {
    'almor-msa': {
        'path': os.path.join(_DATABASES_DIR, 'almor-msa', 'almor-msa-r13.db'),
        'version': 'r13'
    }
}

_LEMMA_SPLIT_RE = re.compile(r'-|_')


CalimaStarDBFlags = namedtuple('CalimaStarDBFlags', ['analysis', 'generation',
                                                     'reinflection'])


class CalimaStarDB:
    """Class providing indexes from a given CALIMA Star database file.

    Args:
        fpath (:obj:`str`): File path to database.
        flags (:obj:`str`): Flag string (similar to opening files) indicates
            what components the database will be used for. 'a' indicates
            analysis, 'g' indicates generation, and 'r' indicates indicates
            reinflection. 'r' is equivalent to 'rg' since the reinflector
            uses both analyzer and generator components internally.
            Defaults to 'a'.

    Raises:
        :obj:`~camel_tools.calima_star.errors.InvalidDatabaseFlagError`: When
            an invalid flag value is given.
    """

    @staticmethod
    def list_builtin_dbs():
        """Returns a list of builtin databases in the form of named tuples
        (:obj:`DBListing`) containing a property `name` that can be passed to
        :meth:`builtin_db` and a property `version` indicating the
        version of the provided database.

        Returns:
            :obj:`list` of :obj:`DBListing`: List of builtin databases.
        """

        return [DBListing(db, _DATABASES[db]['version']) for db in _DATABASES]

    @staticmethod
    def builtin_db(dbname='almor-msa', flags='a'):
        """Create a :obj:`CalimaStarDB` instance from one of the builtin
        databases provided.

        Args:
            dbname (:obj:`str`, optional): Name of builtin database.
                You can use :meth:`list_builtin_dbs` to get a list of
                builtin databases or see :ref:`calima_star_databases`.
                Defaults to 'almor-msa'.
            flags (:obj:`str`, optional): Flag string to be passed to
                :obj:`CalimaStarDB` constructor. Defaults to 'a'.

        Returns:
            :obj:`CalimaStarDB`: Instance of builtin database with given flags.

        Raises:
            :obj:`~camel_tools.calima_star.errors.InvalidBuiltinDatabaseName`:
                When an invalid value for **dbname** is provided.
        """

        if dbname not in _DATABASES:
            raise InvalidBuiltinDatabaseName(dbname)

        return CalimaStarDB(_DATABASES[dbname]['path'], flags)

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

        self.flags = CalimaStarDBFlags(self._withAnalysis,
                                       self._withGeneration,
                                       self._withGeneration)
        self.defines = {}
        self.defaults = {}
        self.order = None
        self.compute_feats = set()
        self.stem_backoffs = {}

        self.prefix_hash = {} if self._withAnalysis else None
        self.suffix_hash = {} if self._withAnalysis else None
        self.stem_hash = {} if self._withAnalysis else None

        self.prefix_cat_hash = {} if self._withGeneration else None
        self.suffix_cat_hash = {} if self._withGeneration else None
        self.lemma_hash = {} if self._withGeneration else None

        self.prefix_stem_compat = {} if self._withAnalysis else None
        self.stem_suffix_compat = {}
        self.prefix_suffix_compat = {}
        self.stem_prefix_compat = {} if self._withGeneration else None
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
                continue

            feat = subtoks[0]
            val = ':'.join(subtoks[1:])

            if val == 'na':
                continue
            elif val == '*':
                res[feat] = None
            else:
                res[feat] = val

        return res

    def _parse_dbfile(self, fpath):
        with open(fpath, 'r') as dbfile:
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

                if line == '###STEMBACKOFF###':
                    self.compute_feats.update(self.order)
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

                if self._withAnalysis:
                    if stem not in self.stem_hash:
                        self.stem_hash[stem] = []
                    self.stem_hash[stem].append((category, analysis))

                if self._withGeneration:
                    # FIXME: Make sure analyses for category are unique?
                    lemma = analysis['lex']
                    lemma_key = _LEMMA_SPLIT_RE.split(lemma)[0]
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
