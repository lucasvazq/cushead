#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module used to validate if anything meets specific requirements"""

import os
from os import path
import sys

from src2.helpers import error_message


class FilesValidator:
    """Handle File System Objects validations"""        

    def __init__(self, file_path, key):
        self.file_path = file_path
        self.key = key
        self.full_path = path.join(os.getcwd(), self.file_path)

    def path_exists(self):
        """Check if path exists"""
        if not path.exists(self.file_path):
            exception = (
                f"'{self.key}' ({self.file_path}) must be referred to a path "
                "that exists.\n"
                f"PATH: {self.full_path}"
            )
            error_message(exception)

    def path_is_file(self):
        """Check if path is not directory"""
        self.path_exists()
        if not path.isfile(self.file_path):
            exception = (
                f"'{self.key}' key ({self.file_path}) must be referred to a "
                "file path that exists.\n"
                f"FILE PATH: {self.full_path}"
            )
            error_message(exception)


class KeysValidator:
    """Handle keys related validations"""

    def __init__(self, key, dictionary=None, value=None):
        self.key = key
        self.dictionary = dictionary
        self.value = value

    def key_exists(self):
        """Check if key is in dictionary"""
        if self.key not in self.dictionary:
            error_message(f"Miss '{self.key}' key and it's required in config "
                           "file.")

    def key_is_not_void(self):
        """Check if key in dictionary is void"""
        if not self.value:
            error_message(f"'{self.key}' key value can't be void.")
