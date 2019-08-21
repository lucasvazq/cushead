#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from os import path
from shutil import copyfile

from .console import DEFAULT_COLOR, ERROR_COLOR


class Errors:

    @staticmethod
    def error_message(message):
        print(f"{ERROR_COLOR}{message}{DEFAULT_COLOR}")
        sys.exit()

    @classmethod
    def exists(cls, relative_path, keyname):
        ffpath = path.join(os.getcwd(), relative_path)
        if not path.exists(ffpath):
            e = (
                f"'{keyname}' ({relative_path}) must be referred to a path "
                "that exists.\n"
                f"PATH: {ffpath}"
            )
            cls.error_message(e)

    @classmethod
    def is_file(cls, relative_path, keyname):
        filepath = path.join(os.getcwd(), relative_path)
        if not path.isfile(filepath):
            e = (
                f"'{keyname}' key ({relative_path}) must be referred to a file "
                "path that exists.\n"
                f"FILE PATH: {filepath}"
            )
            cls.error_message(e)

    @classmethod
    def required_key(cls, dictionary, keyname):
        if keyname not in dictionary:
            cls.error_message("Miss '{keyname}' key and it's required.")

    @classmethod
    def void_key(cls, key, keyname):
        if not len(key):
            cls.error_message(f"'{keyname}' key value can't be void.")


class FilesHelper:

    @staticmethod
    def copy_file(source, destination):
        copyfile(source, destination)

    @staticmethod
    def write_file(filepath, content):
        file_handle = open(filepath, 'w')
        file_handle.write(content)
        file_handle.close()


class FoldersHelper:

    @staticmethod
    def create_folder(folderpath):
        os.makedirs(folderpath, exist_ok=True)
