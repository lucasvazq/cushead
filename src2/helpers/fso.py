#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Disable the Pylint warning about the number of public methods in a class.
# The class FolderHelpers have only one public method, but that method needs to
# be inside a class to keep the code organized.
# pylint: disable=R0903

"""
Helper module related to the File System Objects:
    - Directories
    - Files that aren't directories
"""

import os
from os import path
from shutil import copyfile


class FilesHelper:
    """Files, that aren't directories, helper class"""
    
    def __init__(self, content=None, destination_file_path=None, source_file_path=None):
        self.content = content
        self.destination_file_path = destination_file_path
        self.source_file_path = source_file_path
        folder_path = path.dirname(destination_file_path)
        if folder_path: FoldersHelper(folder_path).create_folder()

    def copy_file(self):
        """Copy files"""
        copyfile(self.source_file_path, self.destination_file_path)

    def write_file(self):
        """Write files"""
        with open(self.destination_file_path, 'w') as file_instance:
            file_instance.write(self.content)

    def write_binary(self):
        """Write binary files"""
        with open(self.destination_file_path, 'wb') as file_instance:
            file_instance.write(self.content)


class FoldersHelper:
    """Folders helper class"""

    def __init__(self, source_folder_path=None):
        self.source_folder_path = source_folder_path

    def create_folder(self):
        """Create folder"""
        os.makedirs(self.source_folder_path, exist_ok=True)
