#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Arguments handler"""

import os
from os import path

from src2.console.arguments import parse_args
from src2.console.config import get_values
from src2.helpers import FilesHelper, FoldersHelper
from src2.module.__main__ import Main as ModuleMain
from src2.module.presets import Presets
from ..info import get_info

class Main(ModuleMain):
    """Main class of this module"""

    def __init__(self, args):
        self.info = get_info()
        self.args = parse_args(args, self.info)
        if self.args.file: super().__init__(config=get_values(self.args))

    def run(self):
        """Handle the different arguments"""
        if self.args.images:
            self.argument_boolean_image()
        if self.args.file: self.argument_string_file()
        if self.args.preset: self.argument_string_preset()

    # --images
    def argument_boolean_image(self):
        binary_images = self.default_images()
        destination_folder = ''.join(self.args.preset.split('/')[0:-1])
        for binary_image in binary_images:
            file_name = binary_image['filename']
            destination_path = path.join(destination_folder, file_name)
            FilesHelper(destination_file_path=destination_path,
                        content=binary_image['content']).write_binary()

    # -file
    def argument_string_file(self):
        all_files = self.all_files()
        for key in all_files:
            FilesHelper(
                content=all_files[key]['content'],
                destination_file_path=all_files[key]['destination_path']
            ).write_file()
        for image_config in self.default_images_creation_config():
            self.open_image(image_config['source_file_path'])
            self.resize_image(
                image_config['destination_file_path'],
                image_config.get('size', [])
            )

    # -presets
    def argument_string_preset(self):
        default_settings = self.default_settings()
        FilesHelper(destination_file_path=self.args.preset,
                    content=default_settings).write_file()
        fullpath = path.join(os.getcwd(), self.args.preset)
        print(f"CONFIG FILE: {self.args.preset}\n"
              f"FULL PATH: {fullpath}")
