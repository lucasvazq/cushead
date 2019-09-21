#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module used to validate if anything meets specific requirements"""

import os
from os import path
import sys

from src2.helpers import error_message


class FilesValidator:
    """Handle File System Objects validations"""        

    @staticmethod
    def path_exists(relative_path, keyname):
        """Check if path exists"""
        fullpath = path.join(os.getcwd(), relative_path)
        if not path.exists(relative_path):
            exception = (
                f"'{keyname}' ({relative_path}) must be referred to a path "
                "that exists.\n"
                f"PATH: {fullpath}"
            )
            error_message(exception)

    @classmethod
    def path_is_not_directory(cls, relative_path, keyname):
        """Check if path is not directory"""
        fullpath = path.join(os.getcwd(), relative_path)
        if not path.isfile(relative_path):
            exception = (
                f"'{keyname}' key ({relative_path}) must be referred to a "
                "file path that exists.\n"
                f"FILE PATH: {fullpath}"
            )
            error_message(exception)


class KeysValidator:
    """Handle keys related validations"""

    @staticmethod
    def key_is_not_void(key, keyname):
        """Check if key in dictionary is void"""
        if not key:
            error_message(f"'{keyname}' key value can't be void.")

    @staticmethod
    def key_exists(dictionary, keyname):
        """Check if key is in dictionary"""
        if keyname not in dictionary:
            error_message("Miss '{keyname}' key and it's required.")
