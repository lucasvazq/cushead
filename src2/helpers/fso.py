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
    
    def __init__(self, content=None, destination_path=None, source_path=None):
        self.content = content
        self.destination_path = destination_path
        self.source_path = source_path
        folder_path = path.dirname(destination_path)
        if folder_path: FoldersHelper(folder_path).create_folder()

    def copy_file(self):
        """Copy files"""
        copyfile(self.source_path, self.destination_path)

    def write_file(self):
        """Write files"""
        with open(self.destination_path, 'w') as file_instance:
            file_instance.write(self.content)

    def write_binary(self):
        """Write binary files"""
        with open(self.source_path, 'wb') as file_instance:
            file_instance.write(self.content)


class FoldersHelper:
    """Folders helper class"""

    def __init__(self, folder_path=None):
        self.folder_path = folder_path

    def create_folder(self):
        """Create folder"""
        os.makedirs(self.folder_path, exist_ok=True)
