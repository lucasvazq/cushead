"""
Module used to parse console arguments.
"""
import argparse
import pathlib
import textwrap
from typing import List

from src import exceptions
from src import helpers
from src import info


def setup_parser() -> argparse.ArgumentParser:
    """
    Setup argparse.

    Returns:
        Argparse parser instance.
    """
    name = info.PACKAGE_NAME
    parser = argparse.ArgumentParser(
        prog=info.PACKAGE_NAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=f"{info.PACKAGE_NAME} -config FILEPATH",
        epilog=textwrap.dedent(f"""\
            Examples:
            1) Generate default config file with images:
                {name} -default settings.json --images
            2) Run that config:
                {name} -config settings.json
        """),
    )

    required_arguments = parser.add_argument_group("")
    optional_arguments = parser.add_argument_group("optional")

    required_arguments.add_argument(
        "-config",
        metavar="FILEPATH",
        dest="config",
        help="Path to a config file in JSON format. Read a config file and create the main files based on it.",
    )

    required_arguments.add_argument(
        "-default",
        metavar="FILENAME",
        dest="default",
        help="Path to output a default config file. Can use with --images.",
    )

    images_names_list = (image.name for image in helpers.get_assets_list())
    joined_words = helpers.string_list_union(string_list=images_names_list)
    optional_arguments.add_argument(
        "--images",
        dest="images",
        action="store_true",
        help=f"Use with -default. Generate default images that can be used by the settings. This include: {joined_words}",
    )
    parser.set_defaults(images=False)

    return parser


def validate_args(*, parser: argparse.ArgumentParser, args: List[str]) -> argparse.ArgumentParser:
    """
    Validate arguments using argparse parser instance.

    Args:
        parser: parser instance.
        args: list of arguments.

    Returns:
        A validated instance of the parser.

    Raises:
        UnrecognizedArgument: when there's any invalid argument.
        MissRequired: when missing a required argument.
        InvalidCombination: when the combinations of arguments are invalid.
        BadReference: when the arguments reference to a invalid file.
    """

    unrecognized_args = parser.parse_known_args(args)[1]
    if unrecognized_args:
        raise exceptions.UnrecognizedArgument(f"Unrecognized argument {unrecognized_args[0]}.")

    parsed_args = parser.parse_args(args)

    if not (parsed_args.config or parsed_args.default):
        raise exceptions.MissRequired("Miss Required arguments. Use -config or -default. Use -h for help.")
    if parsed_args.config and parsed_args.default:
        raise exceptions.InvalidCombination("Can't use -config and -default arguments together.")
    if parsed_args.images and not parsed_args.default:
        raise exceptions.InvalidCombination("Can't use --images without -default.")
    if parsed_args.config:
        reference = pathlib.Path(parsed_args.config)
        if not reference.exists():
            raise exceptions.BadReference('\n'.join((
                f"'config' key ({reference}) must be referred to a path that exists.",
                f"ABSOLUTE PATH: {reference.absolute()}",
            )))
        if not reference.is_file():
            raise exceptions.BadReference('\n'.join((
                f"'config' key ({reference}) must be referred to a file path.",
                f"ABSOLUTE PATH: {reference.absolute()}",
            )))

    return parsed_args


def parse_args(*, args: List[str]) -> argparse.Namespace:
    """
    Parse arguments using argparse.

    Args:
        args: list of args.

    Returns:
        A validated instance of a argparse parser instance.
    """
    parser = setup_parser()
    return validate_args(parser=parser, args=args)
