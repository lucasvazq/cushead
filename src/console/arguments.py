"""
Module used to parse console arguments.
"""
import argparse
import pathlib
from typing import List

from src import exceptions
from src import info
from src.console import assets


def setup_parser(*, args: List[str]) -> argparse.Namespace:
    """
    Setup argparse.

    Returns:
        Argparse parser instance.
    """
    parser = argparse.ArgumentParser(
        prog=info.PACKAGE_NAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=f"{info.PACKAGE_NAME} {{ --help | {{ --config | --default [ --images ] }} FILE }}",
        allow_abbrev=False,
        add_help=False,
        epilog=(
            "Examples:"
            "\n1) Generate default config file with images:"
            f"\n    {info.PACKAGE_NAME} -default settings.json --images"
            "\n2) Run that config:",
            f"\n    {info.PACKAGE_NAME} -config settings.json"
        ),
    )

    excluding_arguments = parser.add_argument_group("excluding arguments")
    optional_arguments = parser.add_argument_group("optional arguments")
    positional_arguments = parser.add_argument_group("positional arguments")

    excluding_arguments.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this help message and exit.",
    )
    excluding_arguments.add_argument(
        "-c",
        "--config",
        dest="config",
        action="store_true",
        default=False,
        help="Read a config file and create the main files based on it.",
    )
    excluding_arguments.add_argument(
        "-d",
        "--default",
        dest="default",
        action="store_true",
        default=False,
        help="Generate a default config. Can be used with --images.",
    )

    images = assets.get_assets_images()
    optional_arguments.add_argument(
        "-i",
        "--images",
        dest="images",
        action="store_true",
        default=False,
        help=(
            f"Use with --default. Generate default images that can be used by the default settings. "
            f"This include: {images.favicon_ico.name}, {images.favicon_png.name}, {images.favicon_svg.name} and {images.preview_png.name}"
        ),
    )

    positional_arguments.add_argument(
        "FILE",
        help=(
            "Input or output file used by --config or --default args. "
            "For --config it must be a path to a config file in JSON format. "
            "For --default it must be the filename that want to create and add there the default config. "
            "If the --images args is setted, the images would be created in the directory of that file."
        )
    )

    return parser.parse_args(args)


def validate_args(*, parser: argparse.ArgumentParser, args: List[str]) -> None:
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

    if not (parser.config or parser.default):
        raise exceptions.MissRequired("Miss Required arguments. Use -c or -d. Use -h for help.")

    if parser.config and parser.default:
        config_arg = '-c' if '-c' in args else '--config'
        default_arg = '-d' if '-d' in args else '--default'
        raise exceptions.InvalidCombination(f"Can't use {config_arg} and {default_arg} arguments together.")

    if parser.images and not parser.default:
        images_arg = '-i' if '-i' in args else '--images'
        raise exceptions.InvalidCombination(f"Can't use {images_arg} without -d.")

    if parser.config:
        reference = pathlib.Path(parser.FILE)
        if not reference.exists():
            raise exceptions.BadReference(
                f"The file ({reference}) must be referred to a path that exists."
                f"\nABSOLUTE PATH: {reference.absolute()}"
            )
        if not reference.is_file():
            raise exceptions.BadReference(
                f"The file ({reference}) must be referred to a file path."
                f"\nABSOLUTE PATH: {reference.absolute()}"
            )


def parse_args(*, args: List[str]) -> argparse.Namespace:
    """
    Parse arguments using argparse.

    Args:
        args: list of args.

    Returns:
        A validated instance of a argparse parser instance.
    """
    parser = setup_parser(args=args)
    validate_args(parser=parser, args=args)
    return parser
