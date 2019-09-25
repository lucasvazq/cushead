#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for handle the arguments passed throught the CLI

Functions:
    parse_args(list) -> object
"""

import textwrap

import argparse

from src2.info import get_info
from src2.helpers import error_message, FilesValidator


def parse_args(args: list) -> object:
    """Argparse main function

    
    This function validate the values of the arguments and, if everythings is
    ok, return object with the arguments as attributes

    Args:
        args list: The arguments. Allowed -config: str, -default: str,
            --images: bool
    """
    info = get_info()
    name = info['package_name']
    parser = argparse.ArgumentParser(
        prog=info['package_name'],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=f"{info['package_name']} -config FILEPATH",
        epilog=textwrap.dedent(f"""\
            Examples:
            1) Generate default config file with images:
                {name} -default settings.json --images
            2) Execute with that config:
                {name} -config settings.json""")
    )

    # ARGUMENTS

    required = parser.add_argument_group("Required (only one)")
    options = parser.add_argument_group("Optional (use with Required "
                                        "arguments)")

    # GROUP: required
    # -default
    required.add_argument(
        '-default',
        metavar='FILENAME',
        dest='default',
        help=(
            "Generate an example config file in JSON format. "
            "That file contains differents variables that can be customized. "
            "Can use with --images"
        )
    )
    # -config
    required.add_argument(
        '-config',
        metavar='FILEPATH',
        dest='config',
        help=(
            "Path to the config file. "
            "Read a config file that contains settings related to SEO and UX "
            "and generate custom files based on that."
        )
    )
    # GROUP: options
    # -images
    options.add_argument(
        '--images',
        dest='images',
        action='store_true',
        help=(
            "Use with -default. "
            "Add example images that can be used by the settings generated "
            "with -config. "
            "This include: favicon_ico_16px.ico, favicon_png_1600px.png,"
            "favicon_svg_scalable.svg and presentation_png_500px.png"
        )
    )

    # Set defaults
    parser.set_defaults(images=False)

    # Validation
    unrecognized = parser.parse_known_args()[1]
    if unrecognized:
        error_message(f"Unrecognized argument {unrecognized[0]}")
    # Need to recall arguments parser.
    # pylint no-member error in child function
    args = parser.parse_args()
    if not (args.default or args.config):
        error_message("Miss Required arguments. Use -default or -config")
    if args.default and args.config:
        error_message("Can't use -default and -config arguments together.")
    if args.images and not args.default:
        error_message("Can't use --images without -default.")
    if args.config:
        FilesValidator(args.config, "-config").path_is_file()

    return args
