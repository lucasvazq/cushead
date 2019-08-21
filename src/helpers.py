#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from os import path
from shutil import copyfile


class Errors:

    @staticmethod
    def error_message(message):
        (COLOR, RESET) = (
            ('', '')
            if os.name == 'nt' else
            (
                '\033[1;31m',  # Red
                '\033[0;0m'  # Default
            )
        )
        print(f"{COLOR}{message}{RESET}")
        sys.exit()

    @classmethod
    def is_file(cls, key, keyname):
        if not path.isfile(key):
            filepath = path.join(os.getcwd(), key)
            e = (
                f"'{keyname}' key ({key}) must be referred to a file path that "
                "exists."
                f"FILE PATH: {filepath}"
            )
            cls.error_message(e)

    @classmethod
    def void_key(cls, key, keyname):
        if not len(key):
            cls.error_message(f"'{keyname}' key value can't be void.")


class FilesHelpers:

    @staticmethod
    def copy_file(source, destination):
        copyfile(source, destination)

    @staticmethod
    def write_file(filepath, content):
        file_handle = open(filepath, 'w')
        file_handle.write(content)
        file_handle.close()


class FoldersHelpers:

    @staticmethod
    def create_folder(folderpath):
        os.makedirs(folderpath, exist_ok=True)
