#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Arguments handler"""

import os
from os import path

from .console.arguments import parse_args
from .helpers import FilesHelper, FoldersHelper
from .info import get_info
from .module.files import Files
from .module.presets import Presets


class Main(Files, Presets):
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
        self.icons_config = (
            icons_config
            if icons_config else
            self.default_icons_config()
        )

    @staticmethod
    def default_icons_config():
        # Order of how icons are generated and added to the head if it's
        # required
        # The order matters
        head_index = [
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
        ]
        browserconfig = {
            'name_ref': 'browserconfig',
            'filename': 'ms-icon',
            'square_sizes': [30, 44, 70, 150, 310],
            'non_square_sizes': [[310, 150]],
        }
        return {
            'head_index': head_index,
            'browserconfig': browserconfig,
        }
