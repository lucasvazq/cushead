#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to handle string transformation

Classes:
    Processors
    Transformators
"""

from typing import List

from src.support import DEFAULT_COLOR, ERROR_COLOR, PRESENTATION_COLOR


class ColorProcessor:
    """Class to handle the color processing

    Init:
        string str = ''

    Methods:
        error_color -> str
        presentation_color -> str
    """

    def __init__(self, string: str = ''):
        self.string = string

    def error_color(self) -> str:
        """Return a string with error color"""
        return ERROR_COLOR + self.string + DEFAULT_COLOR

    def important_color(self) -> str:
        """Return a string with presentation color"""
        return PRESENTATION_COLOR + self.string + DEFAULT_COLOR

    def normal_color(self) -> str:
        return self.string


class Transformators:
    """Class to handle transformation focused on strings

    Init:
        word_list List[str] = None or []

    Methods:
        words_union -> str
    """

    def __init__(self, word_list: List[str] = None or []):
        self.word_list = word_list

    def words_union(self) -> str:
        """Join a word list into a sentence

        Example:
            input = ['foo', 'bar', 'baz', 'etc']
            output = 'foo, bar, baz and etc'
        """
        conactenated_words = ''.join(
            [
                word + (
                    ", " if word in self.word_list[:-2] else (
                        " and " if word == self.word_list[-2] else ""
                    )
                ) for word in self.word_list
            ]
        )
        return conactenated_words
