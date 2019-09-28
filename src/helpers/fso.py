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
    FilesHelper
    FoldersHelper
"""

import os
from os import path
from shutil import copyfile


class FilesHelper:
    """Helper class related to files that aren't directories

    Init:
        destination_file_path str:
        content str = '':
        source_file_path = '':

    Methods:
        copy_file
        write_file
        write_binary

    If the destination path doesn't exists, when calling a method, the entire
    path is created, incluiding folder path and file
    """

    @staticmethod
    def copy_file(destination_file_path: str, source_file_path: str):
        """Copy files"""
        FoldersHelper.create_folder(destination_file_path)
        copyfile(source_file_path, destination_file_path)

    @staticmethod
    def write_file(content: str, destination_file_path: str):
        """Write files"""
        FoldersHelper.create_folder(destination_file_path)
        with open(destination_file_path, 'w') as file_instance:
            file_instance.write(content)

    @staticmethod
    def write_binary(content: bytes, destination_file_path: str):
        """Write binary files"""
        FoldersHelper.create_folder(destination_file_path)
        with open(destination_file_path, 'wb') as file_instance:
            file_instance.write(content)


class FoldersHelper:
    """Folders helper class"""

    @staticmethod
    def create_folder(fso_path: str):
        """Create folder

        The argument can be folder or file path. This method create the dirpath
        of that path.
        """
        os.makedirs(path.dirname(fso_path), exist_ok=True)
