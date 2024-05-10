#!/usr/bin/env python3
"""Module to represent a caching system."""
from collections import OrderedDict

BaseCaching = __import__("base_caching").BaseCaching


class LRUCache(BaseCaching):
    """class for basic caching implementation."""

    def __init__(self):
        """Initialize the instance."""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Add an item to the cache."""
        if key is None or item is None:
            return

        if key not in self.cache_data:
            if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                discarded_key, _ = self.cache_data.popitem(True)
                print("DISCARD: {}".format(discarded_key))
            self.cache_data[key] = item
            self.cache_data.move_to_end(key, last=False)
        else:
            self.cache_data[key] = item

    def get(self, key):
        """Get an item by key from cache."""
        if key in self.cache_data:
            self.cache_data.move_to_end(key, last=False)
        return self.cache_data.get(key, None)
