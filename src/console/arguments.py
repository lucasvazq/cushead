#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module used to handle the argparse library

Classes:
    Argparse
"""
import argparse
import textwrap
from argparse import Namespace
from typing import Union

from src.helpers.assets import Images
from src.helpers.strings import Transformator
from src.helpers.validators import FilesValidator
from src.info import Info
from src.services.logs import Logs


class Argparse(Info, Logs):
    """Class used to handle argparse

    Methods:
        parse_args
    """

    def parse_args(self, args: Union[list, None] = None) -> Namespace:
        """Argparse implementation

        This function validates the values of arguments and, if everything is
        ok, return an object with the arguments as attributes
        """
        if not isinstance(args, list):
            args = []

        info = self.get_info()
        name = info["package_name"]
        parser = argparse.ArgumentParser(
            prog=info["package_name"],
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage=f"{info['package_name']} -config FILEPATH",
            epilog=textwrap.dedent(
                f"""\
                Examples:
                1) Generate default config file with images:
                    {name} -default settings.json --images
                2) Run that config:
                    {name} -config settings.json"""
            ),
        )

        # ARGUMENTS

        main_arguments = parser.add_argument_group("Main arguments")
        complementary_arguments = parser.add_argument_group("Complementary")

        # GROUP: required
        # -config
        main_arguments.add_argument(
            "-config",
            metavar="FILEPATH",
            dest="config",
            help=(
                "Path to a config file in JSON format. "
                "Read a config file and create the main files based on it."
            ),
        )
        # -default
        main_arguments.add_argument(
            "-default",
            metavar="FILENAME",
            dest="default",
            help=(
                "Path to output a default config file. Can use with --images"
            ),
        )
        # GROUP: options
        # -images
        image_list = Images.images_list()
        class_instance = Transformator(string_list=image_list)
        joined_words = class_instance.string_list_union()
        complementary_arguments.add_argument(
            "--images",
            dest="images",
            action="store_true",
            help=(
                f"Use with -default. "
                f"Generate default images that can be used by the settings. "
                f"This include: {joined_words}"
            ),
        )

        # Set defaults
        parser.set_defaults(images=False)

        # Validation
        unrecognized = parser.parse_known_args(args)[1]
        if unrecognized:
            self.error_log(f"Unrecognized argument {unrecognized[0]}")
        # Need to recall arguments parser.
        # pylint no-member error in child function
        parsed_args = parser.parse_args(args)
        if not (parsed_args.config or parsed_args.default):
            self.error_log("Miss Required arguments. Use -config or -default")
        if parsed_args.config and parsed_args.default:
            self.error_log(
                "Can't use -config and -default arguments together."
            )
        if parsed_args.images and not parsed_args.default:
            self.error_log("Can't use --images without -default.")
        if parsed_args.config:
            validator = FilesValidator(
                file_path=parsed_args.config, key="-config"
            )
            validation = validator.path_is_not_directory()
            if validation:
                self.error_log(validation)

        return parsed_args
