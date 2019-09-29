#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to handle the images configurations

Classes:
    DefaultImagesCreationConfig
    DefaultIconsFormatConfig
"""

from os import path
from typing import Dict, List, Union

from src.services.images import ImageService


class DefaultImagesCreationConfig(ImageService):
    """Class to handle the default configuration used for images creation

    Methods:
        default_images_creation_config
            -> List[Dict[str, Union[List[int], bool, str]]]:
    """
    config = {}
    icons_config = {}

    def _favicon_ico(self) -> List[Dict[str, Union[List[int], bool, str]]]:
        favicon_ico = self.config.get('favicon_ico', '')
        if not favicon_ico:
            return []
        destination_file_path = path.join(
            self.config.get('output_folder_path'),
            'favicon.ico',
        ),
        source_file_path = path.join(self.config.get('main_folder_path', ''),
                                     favicon_ico)
        return [{
            'destination_file_path': destination_file_path,
            'resize': False,
            'size': [],
            'source_file_path': source_file_path,
        }]

    def _favicon_png(self) -> List[Dict[str, Union[List[int], bool, str]]]:
        images_format = []
        favicon_png = self.config.get('favicon_png', '')
        if not favicon_png:
            return images_format
        destination_file_path_unformatted = path.join(
            self.config.get('static_folder_path', ''), "{}-{}x{}.png"
        )
        source_file_path = path.join(self.config.get('main_folder_path', ''),
                                     favicon_png)
        for brand_icon_config in self.icons_config.get('favicon_png', []):
            file_name = brand_icon_config.get('file_name', '')
            for size in self.format_sizes(brand_icon_config):
                destination_file_path = (
                    destination_file_path_unformatted.format(file_name,
                                                             size[0], size[1])
                )
                images_format.append({
                    'destination_file_path': destination_file_path,
                    'resize': True,
                    'size': size,
                    'source_file_path': source_file_path,
                })
        return images_format

    def _favicon_svg(self) -> List[Dict[str, Union[List[int], bool, str]]]:
        favicon_svg = self.config.get('favicon_svg', '')
        if not favicon_svg:
            return []
        destination_file_path = path.join(
            self.config.get('static_folder_path'),
            'favicon.svg',
        )
        source_file_path = path.join(self.config.get('main_folder_path'),
                                     favicon_svg)
        return [{
            'destination_file_path': destination_file_path,
            'resize': False,
            'size': [],
            'source_file_path': source_file_path,
        }]

    def _preview_png(self) -> List[Dict[str, Union[List[int], bool, str]]]:
        preview_png = self.config.get('preview_png', '')
        if not preview_png:
            return []
        destination_file_path = path.join(
            self.config.get('static_folder_path'),
            'preview-500x500.png',
        )
        source_file_path = path.join(self.config.get('main_folder_path'),
                                     preview_png)
        return [{
            'destination_file_path': destination_file_path,
            'resize': True,
            'size': [500, 500],
            'source_file_path': source_file_path,
        }]

    def default_images_creation_config(self) \
            -> List[Dict[str, Union[List[int], bool, str]]]:
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
        images_creation_config = [
            self._favicon_ico(),
            self._favicon_png(),
            self._favicon_svg(),
            self._preview_png(),
        ]
        return [
            element for group in images_creation_config
            for element in group
        ]


class IconsFormatConfigStructure:

    def __init__(self,
                 content: str = '',
                 file_name: str = '',
                 file_type: str = '',
                 max_min: List[List[int]] = None or [],
                 metatag: bool = False,
                 name_ref: str = '',
                 non_square_sizes: List[List[int]] = None or [],
                 square_sizes: List[int] = None or [],
                 title: str = '',
                 verbosity: bool = False):
        self.content = content
        self.file_name = file_name
        self.file_type = file_type
        self.max_min = max_min
        self.metatag = metatag
        self.name_ref = name_ref
        self.non_square_sizes = non_square_sizes
        self.square_sizes = square_sizes
        self.title = title
        self.verbosity = verbosity


class DefaultIconsFormatConfig:
    """Class to handle the default icons format configuration

    Methods:
        default_icons_config
            -> Dict[str, Dict[str, Union[List[int], bool, str]]]:
    """
    config: {}

    def _png_icons_config(self):
        yandex_content = (f"logo={self.config.get('static_url', '')}"
                          "/yandex.png, "
                          f"color={self.config.get('background_color', '')}")

        default_favicons_png_config = IconsFormatConfigStructure(
            file_name='favicon',
            name_ref='icon',
            # https://www.favicon-generator.org/
            # https://stackoverflow.com/questions/4014823/does-a-favicon-have-to-be-32x32-or-16x16
            # https://www.emergeinteractive.com/insights/detail/the-essentials-of-favicons/
            square_sizes=[16, 24, 32, 48, 57, 60, 64, 70, 72, 76, 96, 114, 120,
                          128, 144, 150, 152, 167, 180, 192, 195, 196, 228,
                          310],
            file_type='image/png',
            verbosity=True,
        )
        windows_favicon_config = IconsFormatConfigStructure(
            file_name='ms-icon',
            metatag=True,
            name_ref='msapplication-TileImage',
            square_sizes=[144],
        )
        apple_touch_default_config = IconsFormatConfigStructure(
            file_name='apple-touch-icon',
            name_ref='apple-touch-icon',
            square_sizes=[57],
        )
        return [
            # apple touch default
            {
                'name_ref': 'apple-touch-icon',
                'file_name': 'apple-touch-icon',
                'square_sizes': [57],
            },
            # apple touch with differents sizes
            {
                'name_ref': 'apple-touch-icon',
                'file_name': 'apple-touch-icon',
                'square_sizes': [57, 60, 72, 76, 114, 120, 144, 152, 167, 180,
                                 1024],
                'verbosity': True,
            },
            # apple touch startup image default
            {
                'name_ref': 'apple-touch-startup-image',
                'file_name': 'launch',
                'square_sizes': [768],
            },
            # apple touch startup image with differents sizes
            {
                'name_ref': 'apple-touch-startup-image',
                'file_name': 'launch',
                # Based on:
                # https://css-tricks.com/snippets/css/media-queries-for-standard-devices/
                'max_min': [
                    [38, 42],
                    [320, 375],
                    [375, 414],
                    [414, 480],
                    [480, 568],
                    [568, 667],
                    [667, 736],
                    [736, 812],
                    [812, 834],
                    [1024, 1112],
                    [1112, 1200],
                    [1200, 1366],
                    [1366, 1600],
                ],
            },
            # Mac fluid icon
            {
                'name_ref': 'fluid-icon',
                'file_name': 'fluidicon',
                'square_sizes': [512],
                'title': self.config.get('title', ''),
            },
            # yandex browser
            {
                'name_ref': 'yandex-tableau-widget',
                'file_name': 'yandex',
                'square_sizes': [120],
                'metatag': True,
                'content': yandex_content,
            },
        ]

    @staticmethod
    def _browserconfig_icons_config():
        return {
            'name_ref': 'browserconfig',
            'file_name': 'ms-icon',
            'square_sizes': [30, 44, 70, 150, 310],
            'non_square_sizes': [[310, 150]],
        }

    @staticmethod
    def _manifest_icons_config():
        return {
            'name_ref': 'manifest',
            'filename': 'android-icon',
            'square_sizes': [36, 48, 72, 96, 144, 192, 256, 384, 512],
            'file_type': 'image/png',
            'verbosity': True,
        }

    @staticmethod
    def _opensearch_icons_config():
        return {
            'name_ref': 'opensearch',
            'filename': 'opensearch',
            'sqyare_sizes': [16],
            'verbosity': True,
        }

    def default_icons_config(self) \
            -> Dict[str, Dict[str, Union[List[int], bool, str]]]:
        """Return a default icons format configuration

        This return includes configs for favicons with png extension and for
        browserconfig, manifest and opensearch related icons
        """
        return {
            'favicon_png': self._png_icons_config(),
            'browserconfig': self._browserconfig_icons_config(),
            'manifest': self._manifest_icons_config(),
            'opensearch': self._opensearch_icons_config(),
        }

