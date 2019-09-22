#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Arguments handler"""

import os
from os import path

from src2.console.arguments import parse_args
from src2.console.config import get_values
from src2.helpers import FilesHelper, FoldersHelper
from src2.module.main import Main as ModuleMain
from src2.module.presets import Presets
from ..info import get_info


class Main(ModuleMain):
    """Main class of this module"""

    def __init__(self, args):
        self.info = get_info()
        self.args = parse_args(args, self.info)
        if self.args.file:
            self.config = get_values(self.args)
            super().__init__()

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
            FilesHelper(destination_path=destination_path,
                        content=binary_image['content']).write_binary()

    # -file
    def argument_string_file(self):
        print(self.full_index())

    # -presets
    def argument_string_preset(self):
        default_settings = self.default_settings()
        FilesHelper(destination_path=self.args.preset,
                    content=default_settings).write_file()
        fullpath = path.join(os.getcwd(), self.args.preset)
        print(f"CONFIG FILE: {self.args.preset}\n"
              f"FULL PATH: {fullpath}")
