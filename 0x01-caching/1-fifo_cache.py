#!/usr/bin/env python3
"""Module to represent a caching system."""

BaseCaching = __import__("base_caching").BaseCaching


class FIFOCache(BaseCaching):
    """class for basic caching implementation."""

    def __init__(self):
        """Initialize the instance."""
        super().__init__()

    def put(self, key, item):
        """Add an item to the cache."""
        if key and item:
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                discarded_key = next(iter(self.cache_data))
                self.cache_data.pop(discarded_key)
                print("DISCARD: {}".format(discarded_key))

    def get(self, key):
        """Get an item by key from cache."""
        if key in self.cache_data:
            return self.cache_data[key]
        else:
            return None
