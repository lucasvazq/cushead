#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main console module

Classes:
    Main(list)
"""

import os
from os import path

from src2.console.arguments import parse_args
from src2.console.config import get_values
from src2.helpers import FilesHelper, FoldersHelper
from src2.module.__main__ import Main as ModuleMain


class Main(ModuleMain):
    """Class used to run the diferent arguments situation

    Init:
        args list: Arguments, example: ['config', 'settings.json'] for insert
            through the CLI: -config settings.json

    Methods:
        run
        argument_boolean_image
        argument_string_config
        argument_string_default
    """

    def __init__(self, args):
        self.args = parse_args(args)
        if self.args.config: super().__init__(config=get_values(self.args))

    def run(self):
        """Run actual arguments

        Check the current arguments and execute the functions that
        correspond to each one
        """
        if self.args.images:
            self.argument_boolean_image()
        if self.args.config: self.argument_string_config()
        if self.args.default: self.argument_string_default()

    # --images
    def argument_boolean_image(self):
        """Handle --images argument"""
        binary_images = self.default_images()
        destination_folder = ''.join(self.args.default.split('/')[0:-1])
        for binary_image in binary_images:
            file_name = binary_image['filename']
            destination_path = path.join(destination_folder, file_name)
            FilesHelper(destination_file_path=destination_path,
                        content=binary_image['content']).write_binary()

    # -config
    def argument_string_config(self):
        """Handle -config argument"""
        all_files = self.all_files()
        for key in all_files:
            FilesHelper(
                content=all_files[key]['content'],
                destination_file_path=all_files[key]['destination_path']
            ).write_file()
        for image_config in self.default_images_creation_config():
            if image_config.get('resize', False):
                self.resize_image(
                    image_config.get('destination_file_path', ''),
                    image_config.get('source_file_path', ''),
                    image_config.get('size', [])
                )
            else:
                self.move_svg(
                    image_config.get('destination_file_path', ''),
                    image_config.get('source_file_path', '')
                )

    # -default
    def argument_string_default(self):
        """Handle -default argument"""
        default_settings = self.default_settings()
        FilesHelper(destination_file_path=self.args.default,
                    content=default_settings).write_file()
        fullpath = path.join(os.getcwd(), self.args.default)
        print(f"CONFIG FILE: {self.args.default}\n"
              f"FULL PATH: {fullpath}")
