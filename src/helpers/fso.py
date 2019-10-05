#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Disable the Pylint warning about the number of public methods in a class.
# The class FolderHelpers have only one public method, but that method needs to
# be inside a class to keep the code organized.
# pylint:
# disable=R0903

"""
Helper module related to the File System Objects:
    - Directories
    - Files that aren't directories

Classes:
    FoldersHelper
    FilesHelper
"""

import os
from os import path
from shutil import copyfile


class FoldersHelper:
    """Folders helper class

    Init:
        fso_path str = '': path of a file that may or may not be a directory

    Methods:
        create_folder
    """
    def __init__(self, fso_path: str = ''):
        self.fso_path = fso_path

    def create_folder(self):
        """Create folder"""
        os.makedirs(path.dirname(self.fso_path), exist_ok=True)


class FilesHelper(FoldersHelper):
    """Helper class related to files that aren't directories

    Init:
        binary_content bytes = b''
        unicode_content str = ''
        destination_file_path str = ''
        source_file_path str = ''

    Methods:
        copy_file
        write_binary_file
        write_unicode_file

    If the destination path doesn't exist, when calling a method that uses it,
    the entire path is created, including folders
    """

    def __init__(self,
                 binary_content: bytes = b'',
                 unicode_content: str = '',
                 destination_file_path: str = '',
                 source_file_path: str = ''):
        self.binary_content = binary_content
        self.unicode_content = unicode_content
        self.destination_file_path = destination_file_path
        self.source_file_path = source_file_path
        super().__init__(fso_path=self.destination_file_path)

    def copy_file(self):
        """Copy file"""
        self.create_folder()
        copyfile(self.source_file_path, self.destination_file_path)

    def write_binary_file(self):
        """Write binary file"""
        self.create_folder()
        with open(self.destination_file_path, 'wb') as file_instance:
            file_instance.write(self.binary_content)

    def write_unicode_file(self):
        """Write unicode file"""
        self.create_folder()
        with open(self.destination_file_path, 'w') as file_instance:
            file_instance.write(self.unicode_content)
