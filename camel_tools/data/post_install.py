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


from pathlib import Path
from typing import List

from muddler import unmuddle

__all__ = (
    'post_install',
)


def parse_args(arg_types: List[str], args: List[str]):
    result = []
    for arg_type, arg in zip(arg_types, args):
        if arg_type == 'string':
            result.append(arg)
        elif arg_type == 'path':
            result.append(Path(arg))
        elif arg_type == 'int':
            result.append(int(arg))
        elif arg_type == 'float':
            result.append(float(arg))
        elif arg_type == 'bool':
            arg_lower = arg.lower()
            if arg_lower == 'true':
                result.append(True)
            elif arg_lower == 'false':
                result.append(False)
            else:
                # TODO: Throw error
                result.append(False)

    return result


def post_install(config: dict, package_path: Path, args: List[str]):
    parsed_args = parse_args(config['args'], args)

    for step in config['steps']:
        if step['action'] == 'unmuddle':
            source_path = parsed_args[step['source_path_index']]
            muddled_path = Path(package_path, step['muddled_path'])
            output_path = Path(package_path, step['output_path'])
            unmuddle(str(source_path), str(muddled_path), str(output_path))
