"""
Module used to run the package as CLI.
"""
import json
import os
import pathlib
import sys
import textwrap
from json import decoder
from typing import List
from typing import NoReturn
from typing import Tuple


from src import exceptions
from src import helpers
from src import info
from src.console import arguments
from src.console import files_creator
from src.generator import configuration
from src.generator import files


if os.name == "nt":
    _DEFAULT_COLOR = ""
    _ERROR_COLOR = ""
    _PRESENTATION_COLOR = ""
else:
    _DEFAULT_COLOR = "\033[0;0m"
    _ERROR_COLOR = "\033[1;31m"
    _PRESENTATION_COLOR = "\033[1;34m"


def show_presentation() -> NoReturn:
    """
    Print the console presentation message
    """
    presentation_message = textwrap.dedent(f"""\
         ____  _   _  ____   _   _  _____     _     ____     ____ __   __
        / ___|| | | |/ ___| | | | || ____|   / \\   |  _ \\   |  _ \\\\ \\ / /
        | |    | | | |\\___ \\ | |_| ||  _|    / _ \\  | | | |  | |_) |\\ V /
        | |___ | |_| | ___) ||  _  || |___  / ___ \\ | |_| |_ |  __/  | |
        \\____| \\___/ |____/ |_| |_||_____|/_/   \\_\\|____/(_)|_|     |_|
                                    __       _
                                    _/     /
                                    /    __/
                UX / SEO         _/  __/           v {info.PACKAGE_NAME}
                                / __/
                                / /
                                /'

        Author: {info.AUTHOR}
        Email: {info.EMAIL}
        Page: {info.AUTHOR_PAGE}
        License: {info.PACKAGE_LICENSE}

        Source: {info.SOURCE}
        Documentation: {info.DOCUMENTATION}
        For help run: {info.PACKAGE_NAME} -h
    """)
    print(f"{_PRESENTATION_COLOR}{presentation_message}{_DEFAULT_COLOR}")


def generate_default_config_file(*, path: str) -> files.File:
    """
    Return a file ready to save with the default config in JSON format.

    Args:
        path: path where the file should be saved.

    Returns:
        The file to save.
    """
    default_config = configuration.get_default_config()
    parsed_settings = json.dumps(default_config, indent=4).encode('utf-8')
    return files.File(
        path=path,
        data=parsed_settings,
    )


def generate_images(*, path: str) -> Tuple[files.File]:
    """
    Return the default images assets

    Args:
        path: path where the images should be saved.

    Returns:
        A tuple of images ready to save.
    """
    destination_folder = pathlib.Path(path).parent
    return (
        files.File(
            path=pathlib.Path(destination_folder, image.name),
            data=image.data,
        ) for image in helpers.get_assets_list()
    )


def read_config_file(*, path: str) -> dict:
    """
    Read config file.

    Args:
        path: config file path.

    Returns:
        The parsed config.

    Raises:
        WrongFileFormat: when the config file isn't in a valid JSON format.
    """
    with open(path, "r") as file:
        file_string = file.read()
    try:
        config = json.loads(file_string)
    except decoder.JSONDecodeError as exception:
        raise exceptions.WrongFileFormat("".join((
            f"Invalid json file format in ({path})",
            f"ABSOLUTE PATH: {path.absolute()}",
            f"Exception: {exception}"
        )))
    return config


def parse_config_file(*, path: str) -> Tuple[files.File]:
    """
    Parse a config file

    Args:
        path: path where the config file is stored

    Returns:
        The files to generate based on the configuration file.
    """
    config_file = read_config_file(path=path)
    files.validate_config(config=config_file)
    parsed_config = files.parse_config(path=pathlib.Path(path).parent, config=config_file)
    return files.generate_files(config=parsed_config)


def parse_args(*, args: List[str]) -> NoReturn:
    """
    Parse the arguments and create the correspondent files.

    Args:
        args: list of arguments
    """
    files_to_create = []
    try:
        parsed_args = arguments.parse_args(args=args)
        if parsed_args.default:
            files_to_create.append(generate_default_config_file(path=parsed_args.default))
        if parsed_args.images:
            files_to_create.extend(generate_images(path=parsed_args.default))
        if parsed_args.config:
            files_to_create.extend(parse_config_file(path=parsed_args.config))
        files_creator.create_files(files_to_create=files_to_create)
    except (KeyboardInterrupt, exceptions.MainException) as exception:
        sys.exit(f"{_ERROR_COLOR}{exception}{_DEFAULT_COLOR}\n")
