#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main console module

Classes:
    Main(list)
"""

import json
from json.decoder import JSONDecodeError
import os
from os import path

from src.console.arguments import parse_args
from src.helpers.logs import stdout_error_report
from src.helpers.fso import FilesHelper
from src.helpers.miscellaneous import OBJECT_INSTANCE, wasa
from src.module.__main__ import Main as ModuleMain
from src.module.config.user import DefaultUserConfig


class Esa:
    file = 'esa'


class Main(ModuleMain, DefaultUserConfig):
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
    args: object

    def __init__(self, args):
        self.error_handler = stdout_error_report
        self.args = parse_args(args, self.error_handler)
        if self.args.file:
            self._read_config()
        user_config, output_path = self._read_config()
        super().__init__(user_config=user_config, output_path=output_path)

    def _read_config(self):
        json_dict = {}
        output_path = ''
        if not self.args.file:
            return json_dict, output_path
        with open(self.args.file, 'r') as file_instance:
            file_string = file_instance.read()
        try:
            json_dict = json.loads(file_string)
        except JSONDecodeError:
            config_file_fullpath = path.join(os.getcwd(), self.args.file)
            exception = (
                f"Invalid json file format in ({self.args.file})\n"
                f"FILE PATH: {config_file_fullpath}"
            )
            self.error_handler(exception)
        output_path = path.dirname(self.args.file)
        return json_dict, output_path


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
            FilesHelper.write_binary(content=binary_image['content'],
                                     destination_file_path=destination_path)

    # -config
    def argument_string_config(self):
        """Handle -config argument"""
        all_files = self.all_files()
        for key in all_files:
            FilesHelper.write_file(
                content=all_files[key]['content'],
                destination_file_path=all_files[key]['destination_path'],
            )
        for image_config in self.default_images_creation_config():
            if image_config.get('resize', False):
                self.resize_image(
                    image_config.get('destination_file_path', ''),
                    image_config.get('source_file_path', ''),
                    image_config.get('size', []),
                )
            else:
                self.move_svg(
                    image_config.get('destination_file_path', ''),
                    image_config.get('source_file_path', ''),
                )

    # -default
    def argument_string_default(self):
        """Handle -default argument"""
        default_settings = self.default_settings()
        FilesHelper.write_file(destination_file_path=self.args.default,
                               content=default_settings)
        fullpath = path.join(os.getcwd(), self.args.default)
        print(f"CONFIG FILE: {self.args.default}\n"
              f"FULL PATH: {fullpath}")
