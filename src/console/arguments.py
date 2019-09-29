#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module used to handle the argparse library

Classes:
    Argparse
"""

import textwrap

import argparse
from argparse import Namespace

from src.info import Info
from src.helpers.assets import Images
from src.helpers.strings import Transformators
from src.helpers.validators import FilesValidator
from src.services.logs import Logs


class Argparse(Info, Logs):
    """Class used to handle argparse

    Methods:
        parse_args(list) -> Namespace

    Namespace is an argparse class
    """

    def parse_args(self, args: list) -> Namespace:
        """Argparse implementation

        This function validates the values of the arguments and, if everything
        is ok, return an object with the arguments as attributes

        Args:
            args list: The arguments
        """
        info = self.get_info()
        name = info['package_name']
        parser = argparse.ArgumentParser(
            prog=info['package_name'],
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage=f"{info['package_name']} -config FILEPATH",
            epilog=textwrap.dedent(f"""\
                Examples:
                1) Generate default config file with images:
                    {name} -default settings.json --images
                2) Run that config:
                    {name} -config settings.json""")
        )

        # ARGUMENTS

        main_arguments = parser.add_argument_group("Main arguments")
        complementary_arguments = parser.add_argument_group("Complementary")

        # GROUP: required
        # -config
        main_arguments.add_argument(
            '-config',
            metavar='FILEPATH',
            dest='config',
            help=(
                "Path to a config file in JSON format. "
                "Read a config file and create the main files based on it."
            )
        )
        # -default
        main_arguments.add_argument(
            '-default',
            metavar='FILENAME',
            dest='default',
            help=(
                "Path to output a default config file. Can use with --images"
            )
        )
        # GROUP: options
        # -images
        image_list = Images.images_list()
        class_instance = Transformators(word_list=image_list)
        joined_words = class_instance.words_union()
        complementary_arguments.add_argument(
            '--images',
            dest='images',
            action='store_true',
            help=(
                f"Use with -default. "
                f"Generate default images that can be used by the settings. "
                f"This include: {joined_words}"
            )
        )

        # Set defaults
        parser.set_defaults(images=False)

        # Validation
        unrecognized = parser.parse_known_args(args)[1]
        if unrecognized:
            self.error(f"Unrecognized argument {unrecognized[0]}")
        # Need to recall arguments parser.
        # pylint no-member error in child function
        args = parser.parse_args()
        if not (args.config or args.default):
            self.error("Miss Required arguments. Use -config or "
                       "-default")
        if args.config and args.default:
            self.error("Can't use -config and -default arguments "
                       "together.")
        if args.images and not args.default:
            self.error("Can't use --images without -default.")
        if args.config:
            FilesValidator(file_path=args.config, key='-config').path_is_file()

        return args
