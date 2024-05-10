#!/usr/bin/env python3

BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    super.__init__()

    def put(self, key, item):
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        if key in self.cache_data:
            return self.cache_data[key]
        else:
            return None