"""
Module used to parse console arguments.
"""
import argparse
import pathlib
from typing import List

from cushead import exceptions
from cushead import info
from cushead.console import assets


def setup_parser() -> argparse.ArgumentParser:
    """
    Setup argparse.

    Args:
        args: list of args.

    Returns:
        Argparse parser instance.
    """
    parser = argparse.ArgumentParser(
        prog=info.PACKAGE_NAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=f"{info.PACKAGE_NAME} {{ --help | {{ --config | --default [ --images ] }} FILE }}",
        allow_abbrev=False,
        add_help=False,
        epilog="\n".join(
            (
                "Examples:",
                "1) Generate default config file with images:",
                f"    {info.PACKAGE_NAME} -d -i config.json",
                "2) Run that config:",
                f"    {info.PACKAGE_NAME} -c config.json",
            ),
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
            f"Use with --default. Generate default images that can be used by the default config file. "
            f"This include: {images.favicon_ico.name}, {images.favicon_png.name}, {images.favicon_svg.name} and {images.preview_png.name}"
        ),
    )

    positional_arguments.add_argument(
        "FILE",
        nargs="?",
        help=(
            "Input or output file used by --config or --default args. "
            "For --config it must be a path to a config file in JSON format. "
            "For --default it must be the filename that want to create and add there the default config. "
            "If the --images args is setted, the images would be created in the directory of that file."
        ),
    )

    return parser


def validate_args(*, parser_namespace: argparse.Namespace, args: List[str]) -> None:
    """
    Validate arguments using argparse parser instance.

    Args:
        parser_namespace: parser instance.
        args: list of arguments.

    Raises:
        MissRequired: when missing a required argument.
        InvalidCombination: when the combinations of arguments are invalid.
        BadReference: when the arguments reference to a invalid file.
    """
    if not (parser_namespace.config or parser_namespace.default):
        raise exceptions.MissRequired("Miss Required arguments. Use -c or -d. Use -h for help.")

    if parser_namespace.config and parser_namespace.default:
        config_arg = "-c" if "-c" in args else "--config"
        default_arg = "-d" if "-d" in args else "--default"
        raise exceptions.InvalidCombination(f"Can't use {config_arg} and {default_arg} arguments together.")

    if parser_namespace.images and not parser_namespace.default:
        images_arg = "-i" if "-i" in args else "--images"
        raise exceptions.InvalidCombination(f"Can't use {images_arg} without -d.")

    if not (parser_namespace.FILE):
        raise exceptions.MissRequired("Miss FILE")

    if parser_namespace.config:
        reference = pathlib.Path(parser_namespace.FILE)
        if not reference.exists():
            raise exceptions.BadReference(
                "\n".join(
                    (
                        f"The file ({reference}) must be referred to a path that exists.",
                        f"ABSOLUTE PATH: {reference.absolute()}",
                    ),
                ),
            )
        if not reference.is_file():
            raise exceptions.BadReference(
                "\n".join(
                    (
                        f"The file ({reference}) must be referred to a file path.",
                        f"ABSOLUTE PATH: {reference.absolute()}",
                    ),
                ),
            )
