#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to handle string transformation

Classes:
    ColorProcessor
    Transformator
"""

from typing import List

from src.support import DEFAULT_COLOR, ERROR_COLOR, PRESENTATION_COLOR


class ColorProcessor:
    """Class to handle the color processing

    Init:
        string str = ''

    Methods:
        default_color -> str
        error_color -> str
        presentation_color -> str
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
        string_list List[str] = None or []

    Methods:
        string_list_union -> str
    """

    def __init__(self, string_list: List[str] = None or []):
        self.string_list = string_list

    def string_list_union(self) -> str:
        """Join a str list into a sentence

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
