#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Arguments handler"""

import os
from os import path

from ..console.arguments import parse_args
from ..helpers import FilesHelper, FoldersHelper
from ..info import get_info
from ..module.files import Files
from ..module.presets import Presets


class IconsConfig():
    config: dict

    def _png_icons_config(self):
        static_url = self.config.get('static_url', '')
        background_color = self.config.get('background_color', '')
        yandex_content = (
            f"logo={static_url}yandex.png, color={background_color}"
        )
        return [
            # default png favicons
            {
                'name_ref': 'icon',
                'filename': 'favicon',
                # https://www.favicon-generator.org/
                # https://stackoverflow.com/questions/4014823/does-a-favicon-have-to-be-32x32-or-16x16
                # https://www.emergeinteractive.com/insights/detail/the-essentials-of-favicons/
                'square_sizes': [16, 24, 32, 48, 57, 60, 64, 70, 72, 76, 96,
                                114, 120, 128, 144, 150, 152, 167, 180, 192,
                                195, 196, 228, 310],
                'type': 'image/png',
                'verbosity': True,
            },
            # windows favicon
            {
                'name_ref': 'msapplication-TileImage',
                'filename': 'ms-icon',
                'square_sizes': [144],
                'metatag': True,
            },
            # apple touch default
            {
                'name_ref': 'apple-touch-icon',
                'filename': 'apple-touch-icon',
                'square_sizes': [57],
            },
            # apple touch with differents sizes
            {
                'name_ref': 'apple-touch-icon',
                'filename': 'apple-touch-icon',
                'square_sizes': [57, 60, 72, 76, 114, 120, 144, 152, 167, 180,
                                1024],
                'verbosity': True,
            },
            # apple touch startup image default
            {
                'name_ref': 'apple-touch-startup-image',
                'filename': 'launch',
                'square_sizes': [768],
            },
            # apple touch startup image with differents sizes
            {
                'name_ref': 'apple-touch-startup-image',
                'filename': 'launch',
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
                'filename': 'fluidicon',
                'square_sizes': [512],
                'title': self.config.get('title', ''),
            },
            # yandex browser
            {
                'name_ref': 'yandex-tableau-widget',
                'filename': 'yandex',
                'square_sizes': [120],
                'metatag': True,
                'content': yandex_content,
            },
        ]

    def _browserconfig_icons_config(self):
        return {
            'name_ref': 'browserconfig',
            'filename': 'ms-icon',
            'square_sizes': [30, 44, 70, 150, 310],
            'non_square_sizes': [[310, 150]],
        }

    def default_icons_config(self):
        # Order of how icons are generated and added to the head if it's
        # required
        # The order matters

        return {
            'favicon_png': self._png_icons_config(),
            'browserconfig': self._browserconfig_icons_config(),
        }


class Main(Files, IconsConfig, Presets):
    # Head return = head (array), resize (config instances)
    # config is default, can provide custom
    # Can do make_config() # images must exists


    # full(): [files[], resize]
    #   make_html: str
    #       make_head: str
    #           icons
    #           complementary
    #   make browserconfig: str
    #   get_resize: str

    def __init__(self, icons_config=None):
        self.icons_config = icons_config or self.default_icons_config()
