#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to handle the images configurations

Classes:
    IconsFormatConfigStructure
    IconsFormatConfig
"""

from os import path
from typing import Dict, List, Union


class ImageFormatConfig:
    """Class to define attributes of a png image

    Init:
        # basic element
        file_name str = '': output file name

        # head elements

        # basic
        tag_name str = ''
        # normal attributes
        attribute_content str = ''
        attribute_name str = ''
        attribute_rel str = ''
        attribute_type str = ''
        # special attributes
        attribute_special_content: bool = False,
        attribute_special_href: bool = False,
        attribute_special_sizes: bool = False,
        attribute_special_title: bool = False,

        # file sizes
        sizes_max_min: List[List[int]] = None or [],
        sizes_square: List[int] = None or [],
        sizes_rectangular: List[List[int]] = None or []):
    """

    def __init__(self,
                 output_file_name: str = '',
                 output_file_name_size_verbosity: bool = False,
                 output_folder_path: str = '',
                 source_file_path: str = '',
                 sizes_max_min: List[List[int]] = None or [],
                 sizes_square: List[int] = None or [],
                 sizes_rectangular: List[List[int]] = None or [],
                 sizes_mantain: bool = False,
                 url_path: str = '',
                 tag_name: str = '',
                 attribute_content: str = '',
                 attribute_name: str = '',
                 attribute_rel: str = '',
                 attribute_type: str = '',
                 attribute_special_content: bool = False,
                 attribute_special_href: bool = False,
                 attribute_special_sizes: bool = False,
                 attribute_special_title: bool = False):

        # output file name
        self.output_file_name = output_file_name
        self.output_file_name_size_verbosity = output_file_name_size_verbosity
        self.output_folder_path = output_folder_path
        # source
        self.source_file_path = source_file_path
        # sizes
        self.sizes_max_min = sizes_max_min
        self.sizes_square = sizes_square
        self.sizes_rectangular = sizes_rectangular
        self.sizes_mantain = sizes_mantain

        # head elements

        # general
        self.url_path = url_path
        self.tag_name = tag_name
        # normal attributes
        self.attribute_content = attribute_content
        self.attribute_name = attribute_name
        self.attribute_rel = attribute_rel
        self.attribute_type = attribute_type
        # special attributes
        self.attribute_special_content = attribute_special_content
        self.attribute_special_href = attribute_special_href
        self.attribute_special_sizes = attribute_special_sizes
        self.attribute_special_title = attribute_special_title


class IconsFormatConfig:
    """Class to handle the default icons format configuration

    Methods:
        default_icons_config
            -> Dict[str, Dict[str, Union[List[int], bool, str]]]:
    """
    config: {}

    def _favicon_ico_icons_config(self):
        favicon_ico = self.config.get('favicon_ico', '')
        return [
            # <link rel='shortcut icon' href='/favicon.ico' type='image/x-icon' />
            IconsFormatConfig(
                output_file_name='favicon',
                source_file_path=favicon_ico,
                sizes_mantain=True,
                tag_name='link',
                attribute_rel='icon',
                attribute_type='image/x-icon',
                attribute_special_href=True,
            )
        ]

    def _favicon_png_icons_config(self):
        icons = []
        favicon_png = self.config.get('favicon_png', '')
        static_folder_path = self.config.get('static_folder_path', '')
        static_url = self.config.get('static_url', '')

        # Order matters

        # Default png favicon
        # Example:
        # <link rel="icon" type="image/png" href="/static/favicon-16x16.png" sizes="16x16">
        icons.append(
            IconsFormatConfig(
                output_file_name='favicon',
                output_file_name_size_verbosity=True,
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                # https://www.favicon-generator.org/
                # https://stackoverflow.com/questions/4014823/does-a-favicon-have-to-be-32x32-or-16x16
                # https://www.emergeinteractive.com/insights/detail/the-essentials-of-favicons/
                sizes_square=[16, 24, 32, 48, 57, 60, 64, 70, 72, 76, 96, 114,
                              120, 128, 144, 150, 152, 167, 180, 192, 195, 196,
                              228, 310],
                url_path=static_url,
                tag_name='link',
                attribute_rel='icon',
                attribute_type='image/png',
                attribute_special_sizes=True,
                attribute_special_href=True,
            )
        )

        # Microsoft icon
        # Example:
        # <meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png">
        icons.append(
            IconsFormatConfig(
                output_file_name='ms-icon',
                output_file_name_size_verbosity=True,
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[144],
                url_path=static_url,
                tag_name='meta',
                attribute_name='msapplication-TileImage',
                attribute_special_content=True,
            )
        )

        # Apple touch default
        # Example:
        # <link rel="apple-touch-icon" href="/static/apple-touch-icon-default-57x57.png">
        icons.append(
            IconsFormatConfig(
                output_file_name='apple-touch-icon',
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[57],
                url_path=static_url,
                tag_name='link',
                attribute_rel='apple-touch-icon',
                attribute_special_href=True,
            )
        )

        # Apple touch with different sizes
        # Example:
        # <link rel="apple-touch-icon" sizes="57x57" href="/static/apple-touch-icon-57x57.png">
        icons.append(
            IconsFormatConfig(
                output_file_name='apple-touch-icon',
                output_file_name_size_verbosity=True,
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[57, 60, 72, 76, 114, 120, 144, 152, 167, 180,
                              1024],
                url_path=static_url,
                tag_name='link',
                attribute_rel='apple-touch-icon',
                attribute_special_href=True,
                attribute_special_sizes=True,
            )
        )

        # Apple touch startup default
        # Example:
        # ???
        icons.append(
            IconsFormatConfig(
                output_file_name='launch',
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[768],
                url_path=static_url,
                tag_name='link',
                attribute_rel='apple-touch-startup-image',
                attribute_special_href=True,
            )
        )

        # Apple touch startup with different sizes
        # Example:
        # ???
        icons.append(
            IconsFormatConfig(
                output_file_name='launch',
                output_file_name_size_verbosity=True,
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                # Based in:
                # https://css-tricks.com/snippets/css/media-queries-for-standard-devices/
                sizes_max_min=[
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
                url_path=static_url,
                tag_name='link',
                attribute_rel='apple-touch-startup-image',
                attribute_special_href=True,
            )
        )

        # Fluid icon
        # Example:
        # <link rel="fluid-icon" href="/static/fluidicon-512x512.png" title="Microsoft">
        icons.append(
            IconsFormatConfig(
                output_file_name='fluid-icon',
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[512],
                url_path=static_url,
                tag_name='link',
                attribute_rel='fluid-icon',
                attribute_special_href=True,
                attribute_special_title=True,
            )
        )

        # Yandex browser special icon
        # Example:
        # ???
        background_color = self.config.get('background_color', '')
        static_url = self.config.get('static_url', '')
        yandex_content = (
            f"logo={static_url}/yandex.png, color={background_color}"
        )
        icons.append(
            IconsFormatConfig(
                output_file_name='yandex',
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[120],
                url_path=static_url,
                tag_name='meta',
                attribute_name='yandex-tableau-widget',
                attribute_content=yandex_content,
            )
        )

        return icons

    def _favicon_svg_icons_config(self):
        favicon_svg = self.config.get('favicon_svg', '')
        static_folder_path = self.config.get('static_folder_path', '')
        static_url = self.config.get('static_url', '')
        return [
            IconsFormatConfig(
                output_file_name='mask-icon',
                output_folder_path=static_folder_path,
                source_file_path=favicon_svg,
                sizes_maintain=True,
                url_path=static_url,
            )
        ]

    def _preview_png_icons_config(self):
        preview_png = self.config.get('preview_png', '')
        static_folder_path = self.config.get('static_folder_path', '')
        static_url = self.config.get('static_url', '')
        return [
            IconsFormatConfig(
                output_file_name='preview',
                output_folder_path=static_folder_path,
                source_file_path=preview_png,
                sizes_square=[500],
                url_path=static_url,
            )
        ]

    def _browserconfig_icons_config(self):
        favicon_png = self.config.get('favicon_png', '')
        static_folder_path = self.config.get('static_folder_path', '')
        return [
            IconsFormatConfig(
                output_file_name='ms-icon',
                output_file_name_size_verbosity=True,
                output_folder_path = static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[30, 44, 70, 150, 310],
                sizes_rectangular=[[310, 150]],
            )
        ]

    def _manifest_icons_config(self):
        favicon_png = self.config.get('favicon_png', '')
        static_folder_path = self.config.get('static_folder_path', '')
        return [
            IconsFormatConfig(
                output_file_name='android-icon',
                output_file_name_size_verbosity=True,
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[36, 48, 72, 96, 144, 192, 256, 384, 512],
                attribute_type='image/png',
            )
        ]

    def _opensearch_icons_config(self):
        favicon_png = self.config.get('favicon_png', '')
        static_folder_path = self.config.get('static_folder_path', '')
        return [
            IconsFormatConfig(
                output_file_name='opensearch',
                output_file_name_size_verbosity=True,
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[16],
                attribute_type='image/png',
            )
        ]

    def default_icons_config(self) \
            -> Dict[str, Dict[str, Union[List[int], bool, str]]]:
        """Return a default icons format configuration

        This return includes configs for favicons with png extension and for
        browserconfig, manifest and opensearch related icons
        """
        return {
            'favicon_ico': self._favicon_ico_icons_config(),
            'favicon_png': self._favicon_png_icons_config(),
            'favicon_svg': self._favicon_svg_icons_config(),
            'preview_png': self._preview_png_icons_config(),

            'browserconfig': self._browserconfig_icons_config(),
            'manifest': self._manifest_icons_config(),
            'opensearch': self._opensearch_icons_config(),
        }
