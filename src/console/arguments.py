#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc
"""
import argparse
import pathlib
import textwrap

from src import helpers
from src import info
from src.console import console


def setup_parser() -> argparse.ArgumentParser:
    """
    doc
    """
    name = info.package_name
    parser = argparse.ArgumentParser(
        prog=info.package_name,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=f"{info.package_name} -config FILEPATH",
        epilog=textwrap.dedent(f"""\
            Examples:
            1) Generate default config file with images:
                {name} -default settings.json --images
            2) Run that config:
                {name} -config settings.json
        """),
    )

    main_arguments = parser.add_argument_group("Main arguments")
    complementary_arguments = parser.add_argument_group("Complementary")

    # GROUP: required
    # -config
    main_arguments.add_argument(
        "-config",
        metavar="FILEPATH",
        dest="config",
        help="Path to a config file in JSON format. Read a config file and create the main files based on it.",
    )
    # -default
    main_arguments.add_argument(
        "-default",
        metavar="FILENAME",
        dest="default",
        help="Path to output a default config file. Can use with --images",
    )

    # GROUP: options
    # -images
    images_names_list = (image.name for image in helpers.get_images_list())
    joined_words = helpers.string_list_union(string_list=images_names_list)
    complementary_arguments.add_argument(
        "--images",
        dest="images",
        action="store_true",
        help=(
            "Use with -default. Generate default images that can be used by the settings. "
            f"This include: {joined_words}"
        ),
    )

    parser.set_defaults(images=False)

    return parser


def validate_args(*, parser: argparse.ArgumentParser, args: list) -> argparse.ArgumentParser:
    """
    doc
    """

    unrecognized_args = parser.parse_known_args(args)[1]
    if unrecognized_args:
        raise console.MainException(f"Unrecognized argument {unrecognized_args[0]}")

    # Re-parse arguments.
    parsed_args = parser.parse_args(args)

    if not (parsed_args.config or parsed_args.default):
        raise console.MainException("Miss Required arguments. Use -config or -default. Use -h for help")
    if parsed_args.config and parsed_args.default:
        raise console.MainException("Can't use -config and -default arguments together.")
    if parsed_args.images and not parsed_args.default:
        raise console.MainException("Can't use --images without -default.")
    if parsed_args.config:
        reference = pathlib.Path(parsed_args.config)
        if not reference.exists():
            raise console.MainException('\n'.join((
                f"'config' key ({reference}) must be referred to a path that exists.",
                f"ABSOLUTE PATH: {reference.absolute()}",
            )))
        if not reference.is_file():
            raise console.MainException('\n'.join((
                f"'config' key ({reference}) must be referred to a file path.",
                f"ABSOLUTE PATH: {reference.absolute()}",
            )))

    return parsed_args


def parse_args(*, args: list) -> argparse.Namespace:
    """
    doc
    """
    parser = setup_parser()
    return validate_args(parser=parser, args=args)
