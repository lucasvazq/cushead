#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module used to validate if anything meets specific requirements

Classes:
    FilesValidator
    KeysValidator
"""

import os
from os import path


class FilesValidator:
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

    def all(self):
        return self.path_exists() or self.path_is_not_directory()

    def path_exists(self):
        """Check if path exists"""
        if not path.exists(self.file_path):
            return (
                f"'{self.key}' ({self.file_path}) must be referred to a path "
                f"that exists.\n"
                f"PATH: {self.full_path}"
            )

    def path_is_not_directory(self):
        """Check if path is not directory"""
        if not path.isfile(self.file_path):
            return (
                f"'{self.key}' key ({self.file_path}) must be referred to a "
                f"file path.\n"
                f"FILE PATH: {self.full_path}"
            )


class KeysValidator:
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

    def __init__(self, dictionary: dict = {}, key: str = '', value: str = ''):
        self.dictionary = dictionary
        self.key = key
        self.value = value

    def all(self):
        """Run all validations"""
        return self.key_exists() or self.key_is_not_void()

    def key_exists(self):
        """Check if a key is in a dictionary"""
        if self.key not in self.dictionary:
            return (
                f"Miss '{self.key}' key and it's required in config file."
            )

    def key_is_not_void(self):
        """Check if a key in dictionary is not void"""
        if not self.value:
            return f"'{self.key}' key value can't be void."
