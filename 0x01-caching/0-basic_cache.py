#!/usr/bin/env python3
"""Module to represent a caching system."""

BaseCaching = __import__("base_caching").BaseCaching


class BasicCache(BaseCaching):
    """class for basic caching implementation."""

    def put(self, key, item):
        """Add an item to the cache."""
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """Get an item by key from cache."""
        if key in self.cache_data:
            return self.cache_data[key]
        else:
            return None
