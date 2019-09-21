#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Arguments handler"""

import os
from os import path

from src2.console.arguments import parse_args
from src2.config import get_values
from src2.head import Head
from src2.helpers import FilesHelper, FoldersHelper
from src2.presets import Presets
from ..info import get_info


class Main(Head, Presets):
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
