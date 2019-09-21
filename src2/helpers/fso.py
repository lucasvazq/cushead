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

    @staticmethod
    def copy_file(source, destination):
        """Copy files"""
        copyfile(source, destination)

    @staticmethod
    def write_file(filepath, content):
        """Write files"""
        with open(filepath, 'w') as fileinstance:
            fileinstance.write(content)


class FoldersHelper:
    """Folders helper class"""

    @staticmethod
    def create_folder(folderpath):
        """Create folder"""
        os.makedirs(folderpath, exist_ok=True)
