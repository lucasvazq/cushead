#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to handle the images configurations

Classes:
    DefaultImagesCreationConfig
    DefaultIconsFormatConfig
"""

from os import path
from typing import Dict, List, Union


class IconsFormatConfigStructure:

    def __init__(self,
            file_name: str = '',
            tag_name: str = '',
            attribute_content: str = '',
            attribute_name: str = '',
            attribute_rel: str = '',
            attribute_type: str = '',
            attribute_special_content: bool = False,
            attribute_special_href: bool = False,
            attribute_special_sizes: bool = False,
            attribute_special_title: str = '',
            sizes_max_min: List[List[int]] = None or [],
            sizes_square: List[int] = None or [],
            sizes_rectangular: List[List[int]] = None or []):

        # file name
        self.file_name = file_name

        # tag name
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

        # sizes
        self.sizes_max_min = sizes_max_min
        self.sizes_square = sizes_square
        self.sizes_rectangular = sizes_rectangular


class IconsFormatConfig:
    """Class to handle the default icons format configuration

    Methods:
        default_icons_config
            -> Dict[str, Dict[str, Union[List[int], bool, str]]]:
    """
    config: {}

    def _png_icons_config(self):
        icons = []

        # Order matters

        # Default png favicon
        # Example:
        # <link rel="icon" type="image/png" href="/static/favicon-16x16.png" sizes="16x16">
        icons.append(
            IconsFormatConfigStructure(
                tag_name='link',
                file_name='favicon',
                attribute_rel='icon',
                attribute_type='image/png',
                attribute_special_sizes=True,
                attribute_special_href=True,
                # https://www.favicon-generator.org/
                # https://stackoverflow.com/questions/4014823/does-a-favicon-have-to-be-32x32-or-16x16
                # https://www.emergeinteractive.com/insights/detail/the-essentials-of-favicons/
                sizes_square=[16, 24, 32, 48, 57, 60, 64, 70, 72, 76, 96, 114,
                              120, 128, 144, 150, 152, 167, 180, 192, 195, 196,
                              228, 310],
            )
        )

        # Microsoft icon
        # Example:
        # <meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png">
        icons.append(
            IconsFormatConfigStructure(
                tag_name='meta',
                file_name='ms-icon',
                attribute_name='msapplication-TileImage',
                attribute_special_content=True,
                sizes_square=[144],
            )
        )

        # Apple touch default
        # Example:
        # <link rel="apple-touch-icon" href="/static/apple-touch-icon-default-57x57.png">
        icons.append(
            IconsFormatConfigStructure(
                tag_name='link',
                file_name='apple-touch-icon',
                attribute_rel='apple-touch-icon',
                attribute_special_href=True,
                sizes_square=[57],
            )
        )

        # Apple touch with different sizes
        # Example:
        # <link rel="apple-touch-icon" sizes="57x57" href="/static/apple-touch-icon-57x57.png">
        icons.append(
            IconsFormatConfigStructure(
                tag_name='link',
                file_name='apple-touch-icon',
                attribute_rel='apple-touch-icon',
                attribute_special_href=True,
                attribute_special_sizes=True,
                sizes_square=[57, 60, 72, 76, 114, 120, 144, 152, 167, 180, 1024],
            )
        )

        # Apple touch startup default
        # Example:
        # ???
        icons.append(
            IconsFormatConfigStructure(
                tag_name='link',
                file_name='launch',
                attribute_rel='apple-touch-startup-image',
                attribute_special_href=True,
                sizes_square=[768],
            )
        )

        # Apple touch startup with different sizes
        # Example:
        # ???
        icons.append(
            IconsFormatConfigStructure(
                tag_name='link',
                file_name='launch',
                attribute_rel='apple-touch-startup-image',
                attribute_special_href=True,
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
                ]
            )
        )

        # Fluid icon
        # Example:
        # <link rel="fluid-icon" href="/static/fluidicon-512x512.png" title="Microsoft">
        icons.append(
            IconsFormatConfigStructure(
                tag_name='link',
                file_name='fluid-icon',
                attribute_rel='fluid-icon',
                attribute_special_href=True,
                attribute_special_title=True,
                sizes_square=[512],
            )
        )

        # Yandex browser special icon
        # Example:
        # ???
        background_color = self.config.get('background_color', '')
        static_url = self.config.get('static_url', '')
        yandex_content = (f"logo={static_url}"
                          f"/yandex-120x120.png, "
                          f"color={background_color}")
        icons.append(
            IconsFormatConfigStructure(
                tag_name='meta',
                file_name='yandex',
                attribute_name='yandex-tableau-widget',
                attribute_content=yandex_content,
                sizes_square=[120],
            )
        )

        return icons

    @staticmethod
    def _browserconfig_icons_config():
        return [
            IconsFormatConfigStructure(
                file_name='ms-icon',
                sizes_square=[30, 44, 70, 150, 310],
                sizes_rectangular=[[310, 150]],
            )
        ]

    @staticmethod
    def _manifest_icons_config():
        return [
            IconsFormatConfigStructure(
                file_name='android-icon',
                attribute_type='image/png',
                sizes_square=[36, 48, 72, 96, 144, 192, 256, 384, 512],
            )
        ]

    @staticmethod
    def _opensearch_icons_config():
        return [
            IconsFormatConfigStructure(
                file_name='opensearch',
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
            'favicon_png': self._png_icons_config(),
            'browserconfig': self._browserconfig_icons_config(),
            'manifest': self._manifest_icons_config(),
            'opensearch': self._opensearch_icons_config(),
        }
