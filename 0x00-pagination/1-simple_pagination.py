#!/usr/bin/env python3
"""Module to implement a simple pagination"""
import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> tuple:
    """
    Function calculates the start and end indexes for pagination.

    Arguments:
        page (int): The current page number.
        page_size (int): The number of items to display per page.

    Returns:
        A tuple containing the start and end indexes for pagination.
    """
    start_index = 0
    end_index = 0
    if page > 0:
        start_index = (page * page_size) - page_size
        end_index = page * page_size
    result = tuple([start_index, end_index])
    return result


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Function to retrieves a specific page of data from the dataset.

        Arguments:
            page (int): The page number to retrieve. Default is 1.
            page_size (int): The number of items to display per page. Default is 10.

        Returns:
            A list of lists representing the data in the requested page.

        Raises:
            AssertionError: If the page or page_size parameters are not positive integers.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        pagination = index_range(page, page_size)
        data_in_page = self.dataset()[pagination[0] : pagination[1]]

        return data_in_page
