#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Argparse"""

import textwrap

import argparse

from .helpers import Errors


def parse_args(args, info):
    """Argparse main function"""

    name = info['package_name']
    parser = argparse.ArgumentParser(
        prog=info['package_name'],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=f"{info['package_name']} -file FILEPATH",
        epilog=textwrap.dedent(f"""\
            Examples:
            1) Generate config file with images:
                {name} -preset settings.json --images
            2) Execute with that config:
                {name} -file settings.json""")
    )

    # ARGUMENTS

    required = parser.add_argument_group("Required (only one)")
    options = parser.add_argument_group("Options (use with Required "
                                        "arguments)")

    # GROUP: required
    # -preset
    required.add_argument(
        '-preset',
        metavar='FILENAME',
        dest='preset',
        help=(
            "Generate an example config file in JSON format. "
            "That file contains differents variables that can be customized. "
            "Can use with --images"
        )
    )
    # -file
    required.add_argument(
        '-file',
        metavar='FILEPATH',
        dest='file',
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
            "Use with -preset. "
            "Add example images that can be used by the settings generated "
            "with -preset. "
            "This include: favicon_ico_16px.ico, favicon_png_1600px.png,"
            "favicon_svg_scalable.svg and presentation_png_500px.png"
        )
    )

    parser.set_defaults(images=False)
    parser = parser.parse_args(args)

    # Validation
    if not (parser.preset or parser.file):
        Errors.error_message("Miss Required arguments. Use -preset or -file")
    if parser.preset and parser.file:
        Errors.error_message("Can't use -preset and -file arguments together.")
    if parser.images and not parser.preset:
        Errors.error_message("Can't use --images without -preset.")
    if parser.file:
        Errors.exists(parser.file, "-file")
        Errors.is_file(parser.file, "-file")

    return parser
