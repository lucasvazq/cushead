#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc
"""
import json
import pathlib
from typing import List, NoReturn, Tuple

from src import helpers
from src.generator import configuration
from src.generator import files
from src.console import arguments
from src.console import files_creator
from src.console import logs


class MainException(Exception):
    """
    doc
    """
    pass


def generate_default_config_file(*, path: str) -> Tuple[files.File]:
    """
    doc
    """
    default_settings = configuration.default_settings()
    parsed_settings = json.dumps(default_settings, indent=4).encode('utf-8')
    return (
        files.File(
            path=path,
            data=parsed_settings,
        ),
    )


def generate_images(*, path: str) -> Tuple[files.File]:
    """
    doc
    """
    destination_folder = pathlib.Path(path).parent
    return (
        files.File(
            path=pathlib.Path(destination_folder, image.name),
            data=image.data,
        ) for image in helpers.get_images_list()
    )


def parse_config_file(*, path: str) -> Tuple[files.File]:
    """
    doc
    """
    config = configuration.read_config_file(path=path)
    return files.generate_files(config=config)


def parse_args(*, args: List[str]) -> NoReturn:
    """
    doc
    """
    files_to_create = []
    try:
        parsed_args = arguments.parse_args(args=args)
        if parsed_args.default:
            files_to_create.extend(generate_default_config_file(path=parsed_args.default))
        if parsed_args.images:
            files_to_create.extend(generate_images(path=parsed_args.default))
        if parsed_args.config:
            files_to_create.extend(parse_config_file(path=parsed_args.config))
        files_creator.create_files(files_to_create=files_to_create)
    except (KeyboardInterrupt, MainException) as exception:
        logs.error_log(message=exception)
