#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module to handle the creation of image files

Classes:
    ImageFilesCreation
"""

from typing import Dict, List, Union

from src.services.images import ImageService


class ImageFilesCreation(ImageService):
    """Class to handle the default configuration used for images creation

    Methods:
        default_icons_creation_config
    """
    config = {}
    icons_config = {}

    def _creation(self) -> Dict[str, Union[str, List[int]]]:
        files = []
        for group in self.icons_config:
            for brand in self.icons_config[group]:
                for size_format in brand.formated:
                    files.append({
                        'file_name': size_format.file_name,
                        'size': size_format.size,
                        'output_folder_path': brand.output_folder_path,
                        'source_file_path': brand.source_file_path,
                    })
        return files

    def get_icons_creation_config(self) \
            -> List[Dict[str, Union[str, List[int]]]]:
        """Return a list with default images creation configuration

        It's include configurations for the images listed in the assets folder

        Default structure of the dicts in the return is:
        {
            'destination_file_path': str,
            'resize': bool,
            'size': list,
            'source_file_path': str,
        }
        """
        icons_creation_config = [
            self._creation()
        ]
        return [
            element for group in icons_creation_config
            for element in group
        ]
