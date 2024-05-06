#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0"""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Function returns a dictionary containing hypermedia pagination.

        Parameters:
        index (int): starting index for the page..
        page_size (int): The number of items per page.

        Returns:
            A dictionary containing the following keys:
            - 'index': The starting index for the page.
            - 'next_index': The index of the next page.
            - 'page_size': The number of items per page.
            - 'data': A list of items for the current page.

        Raises:
            AssertionError: If index is not integer or out of range.
        """
        assert index is None or isinstance(index, int)

        page_data = self.dataset()
        last_index = len(page_data) - 1
        if index is None:
            index = 0
        else:
            assert 0 <= index <= last_index

        next_index = min((index + page_size), (last_index + 1))

        result_dict = {
            "index": index,
            "next_index": next_index,
            "page_size": page_size,
            "data": page_data[index:next_index],
        }

        return result_dict
