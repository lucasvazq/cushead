#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


class Helpers:

    def __init__(self):
        super().__init__()

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

    @staticmethod
    def create_folder(folderpath):
        os.makedirs(folderpath, exist_ok=True)

    @staticmethod
    def write_file(filepath, content):
        file_handle = open(filepath, 'w')
        file_handle.write(content)
        file_handle.close()
