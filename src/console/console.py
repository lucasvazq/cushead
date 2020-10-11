"""
Module used to run the package as CLI.
"""
import json
import pathlib
import sys
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
from src.console import logs
from src.generator import configuration
from src.generator import files


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
        "domain": "sample.com",
        "text_dir": "ltr",
        "title": "Sample",
        "description": "We do things",
        "subject": "Home Page",
        "main_color": "#ff0000",
        "background_color": "#ffffff",
        "author_name": info.AUTHOR,
        "author_email": info.EMAIL,
        "facebook_app_id": "123456",
        "twitter_username": "sample",
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
    images = assets.get_assets_images()
    return (
        files.File(path=path / images.favicon_ico.name, data=images.favicon_ico.data),
        files.File(path=path / images.favicon_png.name, data=images.favicon_png.data),
        files.File(path=path / images.favicon_svg.name, data=images.favicon_svg.data),
        files.File(path=path / images.preview_png.name, data=images.preview_png.data),
    )


def read_config_file(*, path: pathlib.Path) -> Any:
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
            "\n".join(
                (
                    f"Invalid json file format in ({path})",
                    f"ABSOLUTE PATH: {pathlib.Path(path).absolute()}",
                    f"Exception: {exception}",
                ),
            ),
        )
    return config


def parse_config_file(*, path: pathlib.Path) -> Tuple[files.File, ...]:
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
        parser = arguments.parse_args(args=args)

        path = pathlib.Path(parser.FILE)
        if parser.default:
            files_to_create.append(generate_default_config_file(path=path))
        if parser.images:
            files_to_create.extend(generate_images(path=path.parent))
        if parser.config:
            files_to_create.extend(parse_config_file(path=path))

        files_creator.create_files(files_to_create=files_to_create)

    except (KeyboardInterrupt, exceptions.MainException) as exception:
        sys.exit(f"{logs.ERROR_COLOR}{exception}{logs.DEFAULT_COLOR}\n")
