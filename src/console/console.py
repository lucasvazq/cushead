#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main console module

Classes:
    Main
"""

import collections
import json
import os
import typing

import src.base.configuration
import src.base.generator.files
import src.base.logs
import src.console.arguments
import src.helpers


class Console():
    """Class used to handle the CLI inputs and outputs

    Init:
        args typing.Union[list, None] = None: Arguments, example: ['foo', 'bar', 'baz'],
            equivalent to an input of '-foo bar --baz' through the CLI.
            Their respective values are defined with argparse package,
            that executes at init.

    Methods:
        read_user_config
        run
        argument_boolean_image
        argument_string_config
        argument_string_default
    """

    def __init__(self, args: typing.Union[list, None] = None):
        self.presentation_log(src.base.logs.PRESENTATION_MESSAGE)
        self.args = self.parse_args(args or [])

    def _read_user_config(self) -> typing.Tuple[dict, str]:
        """Read user config and validate them"""
        file_path = self.args.config
        key = "-config"
        # :=
        error = src.helpers.path_is_not_directory(file_path, key)
        if error:
            self.error_log(error)
        # :=
        error = src.helpers.path_exists(file_path, key)
        if error:
            self.error_log(error)

        with open(self.args.config, "r") as file_instance:
            file_string = file_instance.read()

        try:
            json_dict = json.loads(file_string)
        except json.decoder.JSONDecodeError:
            full_path = os.path.join(os.getcwd(), self.args.config)
            self.error_log(
                f"Invalid json file format in ({self.args.config})\n"
                f"FILE PATH: {full_path}\n")
        else:
            main_path = os.path.dirname(self.args.config)
            return json_dict, main_path

    def _create_files(self, files_to_create):
        created_files = collections.defaultdict(list)
        for file in files_to_create["text_files"]:
            content = file["content"]
            destination_file_path = file["destination_file_path"]
            src.helpers.write_unicode_file(content, destination_file_path)
            created_files[os.path.normpath(
                os.path.dirname(destination_file_path))].append(
                    os.path.basename(destination_file_path))

        for file in files_to_create["image_files"]:
            destination_file_path = os.path.join(file["output_folder_path"],
                                                 file["file_name"])
            created_files[os.path.normpath(file["output_folder_path"])].append(
                file["file_name"])

            if file["size"]:
                src.helpers.resize_image(
                    file["source_file_path"],
                    destination_file_path,
                    file["size"],
                    file["background_color"],
                )
            else:
                src.helpers.copy_file(file["source_file_path"],
                                      destination_file_path)

        self.default_log("GENERATED FILES:\n\n" f"{os.getcwd()}")
        last_item_created_files = next(reversed(created_files))
        for output_folder_path in created_files:
            folder_conector, folder_extension = ((
                "`", " ") if output_folder_path == last_item_created_files else
                                                 ("|", "|"))
            self.default_log(f" {folder_conector}-- {output_folder_path}")
            for file in created_files[output_folder_path]:
                file_conector = ("`" if
                                 file == created_files[output_folder_path][-1]
                                 else "|")
                self.default_log(
                    f" {folder_extension}    {file_conector}-- {file}")

    # -config
    def argument_string_config(self):
        """Handle -config argument"""
        user_config, main_path = self._read_user_config()
        config = src.base.configuration.UserConfigHandler().transform(
            user_config, main_path)
        icons_formater = src.base.configuration.IconsFormatConfig(config)
        icons_config = icons_formater.get_icons_config()
        initial_data = {
            'config': config,
            'icons_config': icons_config,
            'indentation': src.helpers.INDENTATION,
        }
        self._create_files(
            src.base.generator.files.FilesGenerator(**initial_data).generate())




from typing import List, NoReturn, Iterable, NamedTuple
from src.console import arguments
from src.base import configuration
from src import helpers
import pathlib
from src.base import logs
from src.base import configuration
from src.base.generator import files

class File(NamedTuple):
    """
    doc
    """
    path: str
    data: bytes


def generate_default_config_file(
    *,
    path: str,
) -> Iterable[File]:
    """
    doc
    """
    default_settings = configuration.default_settings()
    parsed_settings = json.dumps(default_settings, indent=4).encode('utf-8')
    return (
        File(
            path=path,
            data=parsed_settings,
        ),
    )


def generate_images(
    *,
    path: str,
) -> Iterable[File]:
    """
    doc
    """
    destination_folder = pathlib.Path(path).parent
    return (
        File(
            path=pathlib.Path(destination_folder, image.name),
            data=image.data,
        ) for image in helpers.get_images_list()
    )


def parse_config_file(
    *,
    path: str,
) -> Iterable[File]:
    """
    doc
    """
    config = configuration.read_config_file(path=path)

    files_to_generate = files.generate_files(config=config)
    # !!!!!!!!!!!!!!! File instances

    return ()


def parse_args(
    *,
    args: List[str],
) -> NoReturn:
    """
    doc
    """
    files_to_create = []
    parsed_args = arguments.parse_args(args=args)
    try:
        if parsed_args.default:
            files_to_create.extend(generate_default_config_file(path=parsed_args.default))
        if parsed_args.images:
            files_to_create.extend(generate_images(path=parsed_args.default))
        if parsed_args.config:
            files_to_create.extend(parse_config_file(path=parsed_args.config))
    except KeyboardInterrupt as exception:
        logs.error_log(message=exception)

    files.create_files(files_to_create=files_to_create)
