"""
Module used to run the package as CLI.
"""
import json
import os
import pathlib
import sys
import textwrap
from json import decoder
from typing import Any
from typing import List
from typing import Tuple
from typing import TypedDict

from src import exceptions
from src import info
from src.console import arguments
from src.console import assets
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


def show_presentation() -> None:
    """
    Print the console presentation message.
    """
    presentation_message = textwrap.dedent(
        f"""\
          ____  _   _  ____   _   _  _____     _     ____     ____ __   __
         / ___|| | | |/ ___| | | | || ____|   / \\   |  _ \\   |  _ \\\\ \\ / /
        | |    | | | |\\___ \\ | |_| ||  _|    / _ \\  | | | |  | |_) |\\ V /
        | |___ | |_| | ___) ||  _  || |___  / ___ \\ | |_| |_ |  __/  | |
         \\____| \\___/ |____/ |_| |_||_____|/_/   \\_\\|____/(_)|_|     |_|
                                     __       _
                                     _/     /
                                    /    __/
                UX / SEO          _/  __/           v {info.PACKAGE_VERSION}
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
        """
    )
    print(f"{_PRESENTATION_COLOR}{presentation_message}{_DEFAULT_COLOR}")


class DefaultConfig(TypedDict):
    """
    The default config structure.
    """

    static_url: str
    favicon_ico: str
    favicon_png: str
    favicon_svg: str
    preview_png: str
    google_tag_manager: str
    language: str
    territory: str
    domain: str
    text_dir: str
    title: str
    description: str
    subject: str
    main_color: str
    background_color: str
    author_name: str
    author_email: str
    facebook_app_id: str
    twitter_username: str
    twitter_user_id: str
    itunes_app_id: str
    itunes_affiliate_data: str


def get_default_config() -> DefaultConfig:
    """
    Generate the default config.

    Returns:
        a dict with the default config.
    """
    images = assets.get_assets_images()
    return {
        "static_url": "/static",
        "favicon_ico": images.favicon_ico.name,
        "favicon_png": images.favicon_png.name,
        "favicon_svg": images.favicon_svg.name,
        "preview_png": images.preview_png.name,
        "google_tag_manager": "GTM-*******",
        "language": "en",
        "territory": "US",
        "domain": "microsoft.com",
        "text_dir": "ltr",
        "title": "Microsoft",
        "description": "Technology Solutions",
        "subject": "Home Page",
        "main_color": "#ff0000",
        "background_color": "#ffffff",
        "author_name": info.AUTHOR,
        "author_email": info.EMAIL,
        "facebook_app_id": "123456",
        "twitter_username": "Microsoft",
        "twitter_user_id": "123456",
        "itunes_app_id": "123456",
        "itunes_affiliate_data": "123456",
    }


def generate_default_config_file(*, path: pathlib.Path) -> files.File:
    """
    Return a file ready to save with the default config in JSON format.

    Args:
        path: path where the file should be saved.

    Returns:
        The file to save.
    """
    default_config = get_default_config()
    parsed_settings = json.dumps(default_config, indent=4).encode("utf-8")
    return files.File(path=path, data=parsed_settings)


def generate_images(*, path: pathlib.Path) -> Tuple[files.File, ...]:
    """
    Return the default images assets.

    Args:
        path: path where the images should be saved.

    Returns:
        A tuple of images ready to save.
    """
    destination_folder = pathlib.Path(path).parent
    images = assets.get_assets_images()
    return (
        files.File(path=destination_folder / images.favicon_ico.name, data=images.favicon_ico.data),
        files.File(path=destination_folder / images.favicon_png.name, data=images.favicon_png.data),
        files.File(path=destination_folder / images.favicon_svg.name, data=images.favicon_svg.data),
        files.File(path=destination_folder / images.preview_png.name, data=images.preview_png.data),
    )


def read_config_file(*, path: str) -> Any:
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
        raise exceptions.WrongFileFormat(
            "".join(
                (
                    f"Invalid json file format in ({path})",
                    f"ABSOLUTE PATH: {pathlib.Path(path).absolute()}",
                    f"Exception: {exception}",
                )
            )
        )
    return config


def parse_config_file(*, path: str) -> Tuple[files.File, ...]:
    """
    Parse a config file.

    Args:
        path: path where the config file is stored.

    Returns:
        The files to generate based on the configuration file.
    """
    config_file = read_config_file(path=path)
    configuration.validate_config(config=config_file)
    parsed_config = configuration.parse_config(path=pathlib.Path(path).parent, config=config_file)
    return files.generate_files(config=parsed_config)


def parse_args(*, args: List[str]) -> None:
    """
    Parse the arguments and create the correspondent files.

    Args:
        args: list of arguments.
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
