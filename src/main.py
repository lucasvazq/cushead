#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Arguments handler"""

import os
from os import path

from .arguments import parse_args
from .config import get_values
from .head import Head
from .helpers import FilesHelper, FoldersHelper
from .presets import Presets


class Main(Head, Presets):
    """Main class of this module"""
    config = {}

    def __init__(self, info, args):
        self.info = info
        self.args = parse_args(args, info)
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
            relative_path = path.dirname(self.args.preset)
            full_path = path.join(os.getcwd(), relative_path)
            print(
                f"PATH: {relative_path}\n"
                f"FULL PATH: {full_path}"
            )
            return '-preset'

        # -file
        else:

            FoldersHelper.create_folder(self.config['files_output'])

            output_filepath = path.join(os.getcwd(),
                                        self.config['files_output'])
            html_filepath = path.join(output_filepath, 'index.html')
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

            static_relative_folderpath = f".{self.config['static_url']}"
            static_relative_folderpath = path.join(self.config['files_output'],
                                                   static_relative_folderpath)
            static_folderpath = path.join(os.getcwd(),
                                          static_relative_folderpath)
            print(
                f"OUTPUT ROOT FILES: {self.config['files_output']}\n"
                f"(full path): {output_filepath}\n"
                f"OUTPUT STATIC FILES: {static_relative_folderpath}\n"
                f"(full path): {static_folderpath}"
            )

            return '-file'
