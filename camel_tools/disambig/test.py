from cachetools import LFUCache, cached
import time

class TestClass:
    def __init__(self):
        self._cache = LFUCache(100000)

    @cached(cache=lambda self: self._cache, key=lambda self, word_dd: word_dd)
    def test_cached(self, word_dd):
        return word_dd


# Example usage:
test = TestClass()
test.test_cached("hello")

test.test_cached("hello")