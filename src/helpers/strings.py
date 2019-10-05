#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to handle string transformation

Classes:
    ColorProcessor
    Transformator
"""

from typing import List, Union

from src.support import DEFAULT_COLOR, ERROR_COLOR, PRESENTATION_COLOR


class ColorProcessor:
    """Class to handle the color processing

    Init:
        string str = ''

    Methods:
        default_color
        error_color
        presentation_color
    """

    def __init__(self, string: str = ''):
        self.string = string

    def default_color(self) -> str:
        """Return a string with the default color"""
        return self.string

    def error_color(self) -> str:
        """Return a string with error color"""
        return ERROR_COLOR + self.string + DEFAULT_COLOR

    def presentation_color(self) -> str:
        """Return a string with presentation color"""
        return PRESENTATION_COLOR + self.string + DEFAULT_COLOR


class Transformator:
    """Class to handle transformations focused on strings

    Init:
        string_list Union[List[str], None] = None

    Methods:
        string_list_union
    """

    def __init__(self, string_list: Union[List[str], None] = None):
        self.string_list = string_list or []

    def string_list_union(self) -> str:
        """Return a str list joined into a sentence

        Example:
            input = ['foo', 'bar', 'baz', 'etc']
            output = 'foo, bar, baz and etc'
        """
        return ''.join([
            string + (
                ", " if string in self.string_list[:-2] else (
                    " and " if string == self.string_list[-2] else ''
                )
            ) for string in self.string_list
        ])
