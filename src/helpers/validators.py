#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module used to validate if anything meets specific requirements

Classes:
    FilesValidator
    KeysValidator
"""

import os
from os import path

from src.services.logs import Logs


class FilesValidator(Logs):
    """Handle File System Objects validations

    Init:
        file_path str = ''
        key str = ''

    Methods:
        path_exists
        path_is_not_directory
    """

    def __init__(self, file_path: str = '', key: str = ''):
        self.file_path = file_path
        self.key = key
        self.full_path = path.join(os.getcwd(), self.file_path)

    def path_exists(self):
        """Check if path exists"""
        if not path.exists(self.file_path):
            exception = (
                f"'{self.key}' ({self.file_path}) must be referred to a path "
                f"that exists.\n"
                f"PATH: {self.full_path}"
            )
            self.error(exception)

    def path_is_not_directory(self):
        """Check if path is not directory"""
        self.path_exists()
        if not path.isfile(self.file_path):
            exception = (
                f"'{self.key}' key ({self.file_path}) must be referred to a "
                f"file path that exists.\n"
                f"FILE PATH: {self.full_path}"
            )
            self.error(exception)


class KeysValidator(Logs):
    """Handle keys related validations

    Init:
        dictionary str = ''
        key str = ''
        value str = ''

    Methods:
        all
        key_exists
        key_is_not_void
    """

    def __init__(self, dictionary: str = '', key: str = '', value: str = ''):
        self.dictionary = dictionary
        self.key = key
        self.value = value

    def all(self):
        """Run all validations"""
        self.key_exists()
        self.key_is_not_void()

    def key_exists(self):
        """Check if a key is in a dictionary"""
        if self.key not in self.dictionary:
            self.error(
                f"Miss '{self.key}' key and it's required in config file."
            )

    def key_is_not_void(self):
        """Check if a key in dictionary is not void"""
        if not self.value:
            self.error(f"'{self.key}' key value can't be void.")
