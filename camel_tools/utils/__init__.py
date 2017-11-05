"""This sub-module provides low-level text processing utilities that are useful
in other sub-modules.
"""

from .stringutils import isunicode

from .charmap import CharMapper
from .charmap import InvalidCharMapKeyError, BuiltinCharMapNotFoundError
