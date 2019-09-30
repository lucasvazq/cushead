#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main console module

Classes:
    Main(list)
"""

import json
import os
from json.decoder import JSONDecodeError
from os import path

from src.console.arguments import Argparse
from src.helpers.fso import FilesHelper
from src.module.__main__ import Main as ModuleMain
from src.module.config.user import DefaultUserConfig
from src.services.logs import Logs, MessagesHandler


class Main(ModuleMain, Argparse, DefaultUserConfig, Logs, MessagesHandler):
    """Class used to handle the CLI inputs and outputs

    Init:
        args list: Arguments, example: ['foo', 'bar', 'baz'], equivalent to an
            input of '-foo bar --baz' through the CLI. Their respective values
            are defined with argparse package, that executes at init.

    Methods:
        run
        argument_boolean_image
        argument_string_config
        argument_string_default
    """

    def __init__(self, args):
        self.error = self.error_stdout
        self.important_stdout(self.presentation_message())
        self.args = self.parse_args(args)
        user_config, output_path = self._read_config()
        super().__init__(user_config=user_config, output_path=output_path)

    def _read_config(self):
        json_dict = {}
        output_path = ''
        if not self.args.config:
            return json_dict, output_path
        with open(self.args.config, 'r') as file_instance:
            file_string = file_instance.read()
        try:
            json_dict = json.loads(file_string)
        except JSONDecodeError:
            config_file_fullpath = path.join(os.getcwd(), self.args.config)
            exception = (
                f"Invalid json file format in ({self.args.config})\n"
                f"FILE PATH: {config_file_fullpath}"
            )
            self.error(exception)
        output_path = path.dirname(self.args.config)
        return json_dict, output_path

    def run(self):
        """Run the current arguments

        Check the current arguments and execute the functions that correspond
        to each one
        """
        if self.args.images:
            self.argument_boolean_image()
        if self.args.config:
            self.argument_string_config()
        if self.args.default:
            self.argument_string_default()

    # --images
    def argument_boolean_image(self):
        """Handle --images argument"""
        binary_images = self.default_images()
        destination_folder = ''.join(self.args.default.split('/')[0:-1])
        for binary_image in binary_images:
            file_name = binary_image['filename']
            destination_file_path = path.join(destination_folder, file_name)
            class_instance = FilesHelper(
                binary_content=binary_image['content'],
                destination_file_path=destination_file_path,
            )
            class_instance.write_binary_file()

    # -config
    def argument_string_config(self):
        """Handle -config argument"""
        all_files = self.all_files()
        for key in all_files:
            class_instance = FilesHelper(
                destination_file_path=all_files[key].get(
                    'destination_file_path', ''),
                unicode_content=all_files[key].get('content', ''),
            )
            class_instance.write_unicode_file()
        for image_config in self.get_icons_creation_config():
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
        self.normal_stdout('esa')

    # -default
    def argument_string_default(self):
        """Handle -default argument"""
        default_settings = self.default_settings()
        class_instance = FilesHelper(destination_file_path=self.args.default,
                                     unicode_content=default_settings)
        class_instance.write_unicode_file()
        fullpath = path.join(os.getcwd(), self.args.default)
        self.normal_stdout(f"CONFIG FILE: {self.args.default}\n"
                           f"FULL PATH: {fullpath}")
