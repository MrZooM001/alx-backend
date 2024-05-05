#!/usr/bin/env python3
"""Module to implement a simple helper function for pagination"""


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
