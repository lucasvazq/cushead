#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Disable the Pylint warning about the number of public methods in a class.
# The class FolderHelpers have only one public method, but that method needs to
# be inside a class to keep the code organized.
# pylint: disable=R0903

"""Helper module"""

import os
from os import path
import sys
from shutil import copyfile

from .console import DEFAULT_COLOR, ERROR_COLOR


class Errors:
    """Handle errors"""

    @staticmethod
    def error_message(message):
        """Print error message"""
        print(f"{ERROR_COLOR}{message}{DEFAULT_COLOR}")
        sys.exit()

    @classmethod
    def exists(cls, relative_path, keyname):
        """Check if path exists"""
        ffpath = path.join(os.getcwd(), relative_path)
        if not path.exists(ffpath):
            exception = (
                f"'{keyname}' ({relative_path}) must be referred to a path "
                "that exists.\n"
                f"PATH: {ffpath}"
            )
            cls.error_message(exception)

    @classmethod
    def is_file(cls, relative_path, keyname):
        """Check if path is file"""
        filepath = path.join(os.getcwd(), relative_path)
        if not path.isfile(filepath):
            exception = (
                f"'{keyname}' key ({relative_path}) must be referred to a "
                "file path that exists.\n"
                f"FILE PATH: {filepath}"
            )
            cls.error_message(exception)

    @classmethod
    def required_key(cls, dictionary, keyname):
        """Check if key is in dictionary"""
        if keyname not in dictionary:
            cls.error_message("Miss '{keyname}' key and it's required.")

    @classmethod
    def void_key(cls, key, keyname):
        """Check if key in dictionary is void"""
        if not key:
            cls.error_message(f"'{keyname}' key value can't be void.")


class FilesHelper:
    """Files related helpers"""

    @staticmethod
    def copy_file(source, destination):
        """Copy files"""
        copyfile(source, destination)

    @staticmethod
    def write_file(filepath, content):
        """Write files"""
        file_handle = open(filepath, 'w')
        file_handle.write(content)
        file_handle.close()


class FoldersHelper:
    """Folders related helpers"""

    @staticmethod
    def create_folder(folderpath):
        """Create folder"""
        os.makedirs(folderpath, exist_ok=True)
