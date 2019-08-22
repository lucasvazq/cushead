#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Argparse"""

import textwrap

import argparse

from .helpers import Errors


def parse_args(info, args):
    """Argparse main function"""

    name = info['package_name']
    parser = argparse.ArgumentParser(
        prog=info['package_name'],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=f"{info['package_name']} -file FILEPATH",
        epilog=textwrap.dedent(f"""\
            Examples:
            1) Generate config file:
                {name} -preset settings.json
            2) Execute with using that config file:
                {name} -file settings.json""")
    )

    # ARGUMENTS

    options = parser.add_argument_group('Options (one required)')

    # -preset
    options.add_argument(
        '-preset',
        metavar='FILENAME',
        dest='preset',
        help=textwrap.dedent("""\
            Name of config file, example = config.json
            Generate an example config file in JSON format. That file contains
            differents variables that can be customized.""")
    )
    # -file
    options.add_argument(
        '-file',
        metavar='FILEPATH',
        dest='file',
        help=textwrap.dedent("""\
            Path to the config file.
            Read a config file that contains settings related to SEO and UX and
            generate custom files based on that.""")
    )

    parser = parser.parse_args(args)

    # Validation
    if not (parser.preset or parser.file):
        Errors.error_message("Miss arguments. Use -preset or -file")
    if parser.preset and parser.file:
        Errors.error_message("Can't use -preset and -file arguments together.")
    if parser.file:
        Errors.exists(parser.file, "-file")
        Errors.is_file(parser.file, "-file")

    return parser
