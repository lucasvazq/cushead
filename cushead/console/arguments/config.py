"""
Handle the config file.
"""
import json
import pathlib
from json import decoder
from typing import Any
from typing import Tuple
from typing import TypedDict

from cushead import exceptions
from cushead import info
from cushead.console.assets import assets
from cushead.generator import config
from cushead.generator import files


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
    Get the default config.

    Returns:
        A dict with the default config.
    """
    images = assets.get_images()
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
    Return a file ready to create with the default config in JSON format.

    Args:
        path: the destination path for the file.

    Returns:
        The file to create.
    """
    return files.File(path=path, data=json.dumps(get_default_config(), indent=4).encode())


def read_config_file(*, path: pathlib.Path) -> Any:
    """
    Read config file.

    Args:
        path: the config file path.

    Returns:
        The parsed config.

    Raises:
        WrongFileFormat: when the config file isn't in a valid JSON format.
    """
    with open(path) as file:
        data = file.read()
    try:
        return json.loads(data)
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


def parse_config_file(*, path: pathlib.Path) -> Tuple[files.File, ...]:
    """
    Parse a config file.

    Args:
        path: path where the config file is stored.

    Returns:
        The files to generate based on the config file.
    """
    config_file = read_config_file(path=path)
    config.validate_config(config=config_file)
    parsed_config = config.parse_config(path=pathlib.Path(path).parent, config=config_file)
    return files.generate_files(config=parsed_config)
