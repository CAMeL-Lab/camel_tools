#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2024 New York University Abu Dhabi
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


"""The CAMeL Tools morphological analyzer, generator, and reinflector.

Usage:
    camel_morphology analyze
                     [-d DATABASE | --db=DATABASE]
                     [-b BACKOFF | --backoff=BACKOFF]
                     [-c | --cache]
                     [-o OUTPUT | --output=OUTPUT] [FILE]
    camel_morphology generate
                     [-d DATABASE | --db=DATABASE]
                     [-b BACKOFF | --backoff=BACKOFF]
                     [-o OUTPUT | --output=OUTPUT] [FILE]
    camel_morphology reinflect
                     [-d DATABASE | --db=DATABASE]
                     [-o OUTPUT | --output=OUTPUT] [FILE]
    camel_morphology (-l | --list)
    camel_morphology (-v | --version)
    camel_morphology (-h | --help)

Options:
  -b BACKOFF --backoff=BACKOFF
        Backoff mode for analyzer and generator. In analyze mode, it can have
        the following values: NONE, NOAN_ALL, NOAN_PROP, ADD_ALL, ADD_PROP.
        In generate mode it can have the following values: NONE, REINFLECT.
        [default: NONE]
  -c --cache
        Cache computed analyses (only in analyze mode).
  -d DATABASE --db=DATABASE
        Morphology database to use. DATABASE could be the name of a builtin
        database or a path to a database file. [default: calima-msa-r13]
  -o OUTPUT --output=OUTPUT
        Output file. If not specified, output will be printed to stdout.
  -l --list
        List builtin databases with their respective versions.
  -h --help
        Show this screen.
  -v --version
        Show version.
"""


from __future__ import absolute_import

import collections
import sys
import re

from docopt import docopt
import six

import camel_tools as camelt
from camel_tools.utils.charsets import AR_DIAC_CHARSET
from camel_tools.utils.stringutils import force_unicode, force_encoding
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.morphology.generator import Generator
from camel_tools.morphology.reinflector import Reinflector
from camel_tools.morphology.errors import DatabaseError, AnalyzerError
from camel_tools.morphology.errors import GeneratorError, MorphologyError


__version__ = camelt.__version__


_ANALYSIS_BACKOFFS = frozenset(('NONE', 'NOAN_ALL', 'NOAN_PROP', 'ADD_ALL',
                                'ADD_PROP'))
_GENARATION_BACKOFFS = frozenset(('NONE', 'REINFLECT'))
_BUILTIN_DBS = frozenset([d.name for d in MorphologyDB.list_builtin_dbs()])
_DEFAULT_DB = 'calima-msa-r13'

_DIAC_RE = re.compile(r'[' + re.escape(u''.join(AR_DIAC_CHARSET)) + r']')


def _tokenize(s):
    return s.split()


def _dediac(word):
    return _DIAC_RE.sub('', word)


def _to_int(s):
    s = str(s)
    try:
        if not s.isdigit():
            return None
        return int(s)
    except Exception:
        return None


def _open_files(finpath, foutpath):
    if finpath is None:
        fin = sys.stdin

    else:
        try:
            fin = open(finpath, 'r', encoding='utf-8')
        except IOError:
            sys.stderr.write('Error: Couldn\'t open input file {}.'
                             '\n'.format(repr(finpath)))
            sys.exit(1)

    if foutpath is None:
        fout = sys.stdout
    else:
        try:
            fout = open(foutpath, 'w', encoding='utf-8')
        except IOError:
            sys.stderr.write('Error: Couldn\'t open output file {}.'
                             '\n'.format(repr(foutpath)))
            if finpath is not None:
                fin.close()
            sys.exit(1)

    return fin, fout


def _list_dbs():
    for db in sorted(MorphologyDB.list_builtin_dbs(), key=lambda d: d.name):
        # TODO: Print versions and descriptions when they are added to catalogue.
        # sys.stdout.write('{}\t{}\n'.format(db.name, db.version))
        sys.stdout.write('{}\n'.format(db.name))


def _serialize_analyses(fout, word, analyses, order, generation=False):
    buff = collections.deque()
    buff.append(u'#{}: {}'.format(u'LEMMA' if generation else u'WORD',
                                  force_unicode(word)))

    if len(analyses) == 0:
        buff.append(u'NO_ANALYSIS')
    else:
        sub_buff = collections.OrderedDict()
        for a in analyses:
            output = u' '.join([u'{}:{}'.format(force_unicode(f),
                                                force_unicode(str(a[f])))
                                for f in order if f in a])
            if output not in sub_buff:
                sub_buff[output] = True
        buff.extend(sub_buff.keys())

    return u'\n'.join(buff)


def _parse_generator_line(line):
    lemma = None
    feats = {}

    tokens = line.strip().split()

    if len(tokens) < 1:
        return None

    lemma = tokens[0]

    for token in tokens[1:]:
        subtokens = token.split(':')
        if len(subtokens) < 2:
            return None
        else:
            feat = subtokens[0]
            val = ':'.join(subtokens[1:])
            feats[feat] = val

    return (lemma, feats)


def _parse_reinflector_line(line):
    word = None
    feats = {}

    tokens = line.strip().split()

    if len(tokens) < 1:
        return None

    word = tokens[0]

    for token in tokens[1:]:
        subtokens = token.split(':')
        if len(subtokens) < 2:
            return None
        else:
            feat = subtokens[0]
            val = ':'.join(subtokens[1:])
            feats[feat] = val

    return (word, feats)


def _analyze(db, fin, fout, backoff, cache):
    if cache:
        analyzer = Analyzer(db, backoff, cache_size=1024)
    else:
        analyzer = Analyzer(db, backoff)

    line = force_unicode(fin.readline())

    while line:
        if len(line) == 0:
            line = force_unicode(fin.readline())
            continue

        line = line.strip()
        tokens = _tokenize(line)

        for token in tokens:
            analyses = analyzer.analyze(token)

            serialized = _serialize_analyses(fout, token, analyses, db.order)

            if six.PY3:
                fout.write(serialized)
            else:
                fout.write(force_encoding(serialized))

            fout.write('\n\n')

        line = force_unicode(fin.readline())


def _generate(db, fin, fout, backoff):
    generator = Generator(db)
    reinflector = Reinflector(db) if backoff == 'REINFLECT' else None

    line = force_unicode(fin.readline())
    line_num = 1

    while line:
        line = line.strip()

        if len(line) == 0:
            line = force_unicode(fin.readline())
            line_num += 1
            continue

        parsed = _parse_generator_line(line)

        if parsed is None:
            if fin is sys.stdin:
                sys.stderr.write('Error: Invalid input line.\n')
            else:
                sys.stderr.write(
                    'Error: Invalid input line ({}).\n'.format(line_num))

        else:
            lemma = parsed[0]
            feats = parsed[1]

            # Make sure lemma and pos are specified first
            if lemma is None:
                if fin is sys.stdin:
                    sys.stderr.write('Error: Missing lex/lemma feature.\n')
                else:
                    sys.stderr.write(
                        'Error: Missing lex/lemma feature. [{}].\n'.format(
                            line_num))
            elif 'pos' not in feats:
                if fin is sys.stdin:
                    sys.stderr.write('Error: Missing pos feature.\n')
                else:
                    sys.stderr.write(
                        'Error: Missing pos feature. [{}]\n'.format(
                            line_num))
            else:
                try:
                    analyses = generator.generate(lemma, feats)

                    if len(analyses) == 0 and backoff == 'REINFLECT':
                        word = _dediac(lemma)
                        analyses = reinflector.reinflect(word, feats)

                    serialized = _serialize_analyses(fout, lemma, analyses,
                                                     db.order, True)

                    if six.PY3:
                        fout.write(serialized)
                    else:
                        fout.write(force_encoding(serialized))

                    fout.write('\n\n')
                except GeneratorError as error:
                    if fin is sys.stdin:
                        sys.stderr.write('Error: {}.\n'.format(error.msg))
                    else:
                        sys.stderr.write('Error: {}. [{}]\n'.format(error.msg,
                                                                    line_num))

        line = force_encoding(fin.readline())
        line_num += 1


def _reinflect(db, fin, fout):
    reinflector = Reinflector(db)

    line = force_unicode(fin.readline())
    line_num = 1

    while line:
        line = line.strip()

        if len(line) == 0:
            line = force_unicode(fin.readline())
            line_num += 1
            continue

        parsed = _parse_reinflector_line(line)

        if parsed is None:
            if fin is sys.stdin:
                sys.stderr.write('Error: Invalid input line.\n')
            else:
                sys.stderr.write(
                    'Error: Invalid input line. [{}]\n'.format(line_num))

        else:
            word = parsed[0]
            feats = parsed[1]

            try:
                analyses = reinflector.reinflect(word, feats)

                serialized = _serialize_analyses(fout, word, analyses,
                                                 db.order)

                if six.PY3:
                    fout.write(serialized)
                else:
                    fout.write(force_encoding(serialized))

                fout.write('\n\n')
            except MorphologyError as error:
                # This could be thrown by the analyzer, generator, or
                # reinflector.
                if fin is sys.stdin:
                    sys.stderr.write('Error: {}.\n'.format(error.msg))
                else:
                    sys.stderr.write('Error: {}. [{}]\n'.format(error.msg,
                                                                line_num))

        line = force_unicode(fin.readline())
        line_num += 1


def main():  # pragma: no cover
    try:
        version = ('CAMeL Tools v{}'.format(__version__))
        arguments = docopt(__doc__, version=version)

        if arguments.get('--list', False):
            _list_dbs()
            sys.exit(1)

        analyze = arguments.get('analyze', False)
        generate = arguments.get('generate', False)
        reinflect = arguments.get('reinflect', False)

        cache = arguments.get('--cache', False)
        backoff = arguments.get('--backoff', 'NONE')

        # Make sure we have a valid backoff mode
        if backoff is None:
            backoff = 'NONE'
        if analyze and backoff not in _ANALYSIS_BACKOFFS:
            sys.stderr.write('Error: invalid backoff mode.\n')
            sys.exit(1)
        if generate and backoff not in _GENARATION_BACKOFFS:
            sys.stderr.write('Error: invalid backoff mode.\n')
            sys.exit(1)

        # Open files (or just use stdin and stdout)
        fin, fout = _open_files(arguments['FILE'], arguments['--output'])

        # Determine required DB flags
        if analyze:
            dbflags = 'a'
        elif generate and backoff == 'NONE':
            dbflags = 'g'
        else:
            dbflags = 'r'

        # Load DB
        try:
            dbname = arguments.get('--db', _DEFAULT_DB)
            if dbname in _BUILTIN_DBS:
                db = MorphologyDB.builtin_db(dbname, dbflags)
            else:
                db = MorphologyDB(dbname, dbflags)
        except DatabaseError:
            sys.stderr.write('Error: Couldn\'t parse database.\n')
            sys.exit(1)
        except IOError:
            sys.stderr.write('Error: Database file could not be read.\n')
            sys.exit(1)

        # Continue execution in requested mode
        if analyze:
            try:
                _analyze(db, fin, fout, backoff, cache)
            except AnalyzerError as error:
                sys.stderr.write('Error: {}\n'.format(error.msg))
                sys.exit(1)
            except IOError:
                sys.stderr.write('Error: An IO error occurred.\n')
                sys.exit(1)

        elif generate:
            try:
                _generate(db, fin, fout, backoff)
            except IOError:
                sys.stderr.write('Error: An IO error occurred.\n')
                sys.exit(1)

        elif reinflect:
            try:
                _reinflect(db, fin, fout)
            except IOError:
                sys.stderr.write('Error: An IO error occurred.\n')
                sys.exit(1)

        sys.exit(0)

    except KeyboardInterrupt:
        sys.stderr.write('Exiting...\n')
        sys.exit(1)
    except Exception:
        sys.stderr.write('Error: An unknown error occurred.\n')
        sys.exit(1)


if __name__ == '__main__':
    main()
