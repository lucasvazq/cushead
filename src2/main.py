#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Arguments handler"""

import os
from os import path

from .console.arguments import parse_args
from .config import get_values
from .files import Files
from .head import Head
from .helpers import FilesHelper, FoldersHelper
from .presets import Presets
from .info import get_info


class Main(Files, Presets):
    # Head return = head (array), resize (config instances)
    # config is default, can provide custom
    # Can do make_config() # images must exists


    # full(): [files[], resize]
    #   make_html: str
    #       make_head: str
    #   make browserconfig: str
    #   get_resize: str

    def __init__(self, images_config=default_icons_config()):
        self.icons_config = images_config

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


class Main2(Head, Presets):
    """Main class of this module"""
    config = {}

    def __init__(self, args):
        self.info = get_info()
        self.args = parse_args(args, self.info)
        if self.args.file:
            self.config = get_values(self.args)
        super().__init__()

    def run(self):
        """Handle the different arguments"""

        # -presets
        if self.args.preset:
            self.settings()
            if self.args.images:
                self.assets()
            fullpath = path.join(os.getcwd(), self.args.preset)
            print(
                f"CONFIG FILE: {self.args.preset}\n"
                f"(full path): {fullpath}"
            )
            return '-preset'

        # -file
        else:

            # Define the main path as the passed throught -file argument
            self.config['main_path'] = path.dirname(self.args.file)

            self.config['output_path'] = path.join(self.config['main_path'],
                                                      'output')
            FoldersHelper.create_folder(self.config['output_path'])
            html_filepath = path.join(self.config['output_path'], 'index.html')

            # Prevent the declare creation of folder in root path if the static
            # url start with a slash
            if self.config['static_url'][0] == '/':
                self.config['static_url'] = self.config['static_url'][1:]
            self.config['static_url_path'] = path.join(
                self.config['output_path'],
                self.config['static_url']
            )
            FoldersHelper.create_folder(self.config['static_url_path'])

            head = self.head_general()

            # Concatenate all head elements in a string
            head = [element for array in head for element in array]
            space = "    "  # four spaces for indentation
            head = ''.join(f"{space * 2}{element}\n" for element in head)
            head = head.replace('\'', '"')

            # Generate html document filestring
            html_lang = (
                f" lang={self.config['language']}"
                if 'language' in self.config else ""
            )
            html_string = (
                "<!DOCTYPE html>\n"
                f"<html{html_lang}>\n"
                f"{space}<head>\n"
                f"{head}"  # already have indentation
                f"{space}</head>\n"
                f"{space}<body>\n"
                f"{space}</body>\n"
                "</html>"
            )

            FilesHelper.write_file(html_filepath, html_string)

            output_fullpath = path.join(os.getcwd(),
                                           self.config['output_path'])
            static_fullpath = path.join(os.getcwd(),
                                          self.config['static_url_path'])
            print(
                f"OUTPUT ROOT FILES: {self.config['output_path']}\n"
                f"(full path): {output_fullpath}\n"
                f"OUTPUT STATIC FILES: {self.config['static_url_path']}\n"
                f"(full path): {static_fullpath}"
            )

            return '-file'
