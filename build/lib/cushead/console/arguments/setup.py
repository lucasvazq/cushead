"""
Handle the argparse related features.
"""
import argparse
import pathlib
from typing import List

from cushead import exceptions
from cushead import info
from cushead.console.assets import assets


def get_parser() -> argparse.ArgumentParser:
    """
    Return the argparse instance.

    Returns:
        An argparse parser instance.
    """
    parser = argparse.ArgumentParser(
        prog=info.PACKAGE_NAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=f"{info.PACKAGE_NAME} {{ --help | {{ --config | --default [ --images ] }} FILE }}",
        allow_abbrev=False,
        add_help=False,
        epilog="\n".join(
            (
                "Example:",
                "1) Generate default config file with images:",
                f"  {info.PACKAGE_NAME} --default --images config.json",
                "2) Run that config:",
                f"  {info.PACKAGE_NAME} --config config.json",
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
        help="Read a config file and create the website template based on it.",
    )
    excluding_arguments.add_argument(
        "-d",
        "--default",
        dest="default",
        action="store_true",
        default=False,
        help="Generate a default config. Can be used with --images.",
    )

    images = assets.get_images()
    optional_arguments.add_argument(
        "-i",
        "--images",
        dest="images",
        action="store_true",
        default=False,
        help=(
            "Use with --default. Generate default images that can be used by the default config file. "
            f"This include: {images.favicon_ico.name}, {images.favicon_png.name}, {images.favicon_svg.name} and {images.preview_png.name}"
        ),
    )

    positional_arguments.add_argument(
        "FILE",
        nargs="?",
        help=(
            "Input or output file used by the --config or --default arguments. "
            "For --config it must be a path to a config file in JSON format. "
            "For --default it must be the destination path where to want to create the default config. "
            "If the --images argument is set, the images would be created in the directory of that file."
        ),
    )

    return parser


def validate_args(*, parser_namespace: argparse.Namespace, args: List[str]) -> None:
    """
    Validate arguments using an argparse parser instance.

    Args:
        parser_namespace: the parser instance.
        args: the list of arguments.

    Raises:
        MissRequired: when missing a required argument.
        InvalidCombination: when the combinations of arguments are invalid.
        BadReference: when the arguments reference an invalid file.
    """
    if not (parser_namespace.config or parser_namespace.default):
        raise exceptions.MissRequired("Missing a required argument. Use --config, --default or --help.")

    if parser_namespace.config and parser_namespace.default:
        config_arg = "-c" if "-c" in args else "--config"
        default_arg = "-d" if "-d" in args else "--default"
        raise exceptions.InvalidCombination(f"Can't use {config_arg} and {default_arg} arguments together.")

    if parser_namespace.images and not parser_namespace.default:
        images_arg = "-i" if "-i" in args else "--images"
        raise exceptions.InvalidCombination(f"Can't use {images_arg} argument without --default.")

    if not parser_namespace.FILE:
        if parser_namespace.config:
            raise exceptions.MissRequired("The path to the config file is missing.")
        raise exceptions.MissRequired("The destination path for the default config file is missing.")

    if parser_namespace.config:
        reference = pathlib.Path(parser_namespace.FILE)
        if not reference.exists():
            raise exceptions.BadReference(
                "\n".join(
                    (
                        f"The file ({reference}) must be a reference to a path that exists.",
                        f"ABSOLUTE PATH: {reference.absolute()}",
                    ),
                ),
            )
        if not reference.is_file():
            raise exceptions.BadReference(
                "\n".join(
                    (
                        f"The file ({reference}) must be a reference to a file.",
                        f"ABSOLUTE PATH: {reference.absolute()}",
                    ),
                ),
            )
