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
            page_size (int): The number of items to display per page.
            Default is 10.

        Returns:
            A list of lists representing the data in the requested page.

        Raises:
            AssertionError: If the page or page_size arguments
            are not positive integers.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        pagination = index_range(page, page_size)
        data_in_page = self.dataset()[pagination[0]:pagination[1]]

        return data_in_page

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """
        Function to retrieve a specific page of data from the dataset,
        along with hypermedia links for next and previous pages.

        Arguments:
            page (int): The page number to retrieve. Default is 1.
            page_size (int): The number of items to display per page.
            Default is 10.

        Returns:
            A dictionary with these key-value pairs:
            - page_size: the length of the returned dataset page
            - page: the current page number
            - data: the dataset page equivalent to return from tasl 1
            - next_page: number of the next page, None if no next page
            - prev_page: number of the previous page, None if no previous page
            - total_pages: total number of pages in the dataset as an integer

        Raises:
            AssertionError: If the page or page_size arguments
            are not positive integers.
        """
        start_index = index_range(page, page_size)[0]
        end_index = index_range(page, page_size)[1]
        page_data = self.get_page(page, page_size)
        hypermedia_result = {
            "page_size": len(page_data),
            "page": page,
            "data": page_data,
            "next_page": page + 1 if end_index < len(self.__dataset) else None,
            "prev_page": page - 1 if start_index > 0 else None,
            "total_page": math.ceil(len(self.__dataset) / page_size),
        }

        return hypermedia_result
