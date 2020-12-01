"""
Interpret the arguments and execute the actions related to each one.
"""
import argparse
import pathlib
import sys
from typing import List
from typing import Tuple

from cushead import exceptions
from cushead.console import logs
from cushead.console.arguments import config
from cushead.console.arguments import files_creator
from cushead.console.arguments import setup
from cushead.console.assets import assets
from cushead.generator import files


def generate_images(*, path: pathlib.Path) -> Tuple[files.File, ...]:
    """
    Get the assets images to create.

    Args:
        path: the destination path for the images.

    Returns:
        A tuple of the images to create.
    """
    images = assets.get_images()
    return (
        files.File(path=path / images.favicon_ico.name, data=images.favicon_ico.data),
        files.File(path=path / images.favicon_png.name, data=images.favicon_png.data),
        files.File(path=path / images.favicon_svg.name, data=images.favicon_svg.data),
        files.File(path=path / images.preview_png.name, data=images.preview_png.data),
    )


def handle_args(*, parser_namespace: argparse.Namespace) -> List[files.File]:
    """
    Handle parser arguments.

    Args:
        parser_namespace: the parser.

    Returns:
        The files to create.
    """
    files_to_create = []
    path = pathlib.Path(parser_namespace.FILE)
    if parser_namespace.default:
        files_to_create.append(config.generate_default_config_file(path=path))
    if parser_namespace.images:
        files_to_create.extend(generate_images(path=path.parent))
    if parser_namespace.config:
        files_to_create.extend(config.parse_config_file(path=path))
    return files_to_create


def parse_args(*, args: List[str]) -> None:
    """
    Parse the arguments and create the corresponding files.

    Args:
        args: the list of arguments.
    """
    parser = setup.get_parser()
    try:
        parser_namespace = parser.parse_args(args=args)
        setup.validate_args(parser_namespace=parser_namespace, args=args)
        files_to_create = handle_args(parser_namespace=parser_namespace)
        files_creator.create_files(files_to_create=files_to_create)
    except (KeyboardInterrupt, exceptions.MainException) as exception:
        sys.exit(logs.get_exception_message(parser=parser, message=str(exception)))
