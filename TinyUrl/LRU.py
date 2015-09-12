from collections import OrderedDict

class LRUCache:
    # @param capacity, an integer
    def __init__(self, capacity):
        self.capacity = capacity
        # use OrderedDict to simulate LRU cache
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            value = self.cache[key]
            # remove key then add it again
            del self.cache[key]
            self.cache[key] = value
            return value
        else:
            return ""

    def set(self, key, value):
        if key in self.cache:
            # remove key if already in cache
            del self.cache[key]
        self.cache[key] = value
        # pop an item (oldest) if cache is full
        if len(self.cache) > self.capacity:
            self.cache.popitem(False)