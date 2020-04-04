#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main console module

Classes:
    Main
"""

import json
import os
import typing

import src_2.console.arguments
import src_2.base.logs
import src_2.base.generator
import src_2.base.configuration
import src_2.helpers


class Console(src_2.console.arguments.Argparse, src_2.base.logs.Logs):
    """Class used to handle the CLI inputs and outputs

    Init:
        args typing.Union[list, None] = None: Arguments, example: ['foo', 'bar', 'baz'],
            equivalent to an input of '-foo bar --baz' through the CLI.
            Their respective values are defined with argparse package,
            that executes at init.

    Methods:
        read_user_config
        run
        argument_boolean_image
        argument_string_config
        argument_string_default
    """

    def __init__(self, args: typing.Union[list, None] = None):
        self.presentation_log(src_2.base.logs.PRESENTATION_MESSAGE)
        self.args = self.parse_args(args or [])

    def _read_user_config(self) -> typing.Tuple[dict, str]:
        """Read user config and validate them"""
        file_path = self.args.config
        key = "-config"
        if error := path_is_not_directory(file_path, key):
            self.error_log(error)
        if error := path_exists(file_path, key):
            self.error_log(error)

        with open(self.args.config, "r") as file_instance:
            file_string = file_instance.read()

        json_dict = {}
        try:
            json_dict.update(json.loads(file_string))
        except json.decoder.JSONDecodeError:
            full_path = os.path.join(os.getcwd(), self.args.config)
            self.error_log(
                f"Invalid json file format in ({self.args.config})\n"
                f"FILE PATH: {full_path}\n"
            )

        main_path = os.path.dirname(self.args.config)
        return json_dict, main_path

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
        src_2.helpers.create_folder(self.args.default)
        binary_images = src_2.base.configuration.default_images()
        destination_folder = os.path.dirname(self.args.default)
        for binary_image in binary_images:
            file_name = binary_image["filename"]
            destination_file_path = os.path.join(destination_folder, file_name)
            src_2.helpers.write_binary_file(binary_image["content"], destination_file_path)

    # -config
    def argument_string_config(self):
        """Handle -config argument"""
        user_config, main_path = self.read_user_config()
        if not user_config and not main_path:
            self.error_log('FALTA USER CONFIG')

        self.config = src_2.base.configuration.UserConfigHandler.transform(user_config, main_path)
        self.icons_config = self.default_icons_config()

        src_2.base.generator.BaseGenerator(self.config).all_files()

        for key in all_files:
            src_2.helpers.write_unicode_file(all_files[key].get("destination_file_path", ""), all_files[key].get("content", ""))
        for image_config in src_2.base.generator.images.Images(self.config, self.icons_config).get_icons_creation_config():
            destination_file_path = os.path.join(
                image_config.get("output_folder_path", ""),
                image_config.get("file_name", ""),
            )
            if image_config.get("size", False):
                src_2.helpers.resize_image(
                    destination_file_path,
                    image_config.get("source_file_path", ""),
                    image_config.get("size", []),
                )
            else:
                src_2.helpers.move_svg(destination_file_path, image_config.get("source_file_path", ""))

    # -default
    def argument_string_default(self):
        """Handle -default argument"""
        default_settings = src_2.base.configuration.default_settings()
        src_2.helpers.write_unicode_file(default_settings, self.args.default)
        fullpath = os.path.join(os.getcwd(), self.args.default)
        self.default_log(f"CONFIG FILE: {self.args.default}\n" f"FULL PATH: {fullpath}")
