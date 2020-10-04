"""
Module where are all things related to the configurations.
"""
import pathlib
import re
from typing import NoReturn
from typing import Optional
from typing import TypedDict
from typing import Union

from PIL import IcoImagePlugin
from PIL import Image
from PIL import PngImagePlugin

import schema

from src import exceptions
from src import helpers
from src import info


class Config(TypedDict):
    """
    The parsed config structure.
    """

    main_folder_path: pathlib.Path
    output_folder_path: pathlib.Path
    static_url: str
    favicon_ico: Optional[IcoImagePlugin.IcoImageFile]
    favicon_png: Optional[PngImagePlugin.PngImageFile]
    favicon_svg: Optional[pathlib.Path]
    preview_png: Optional[PngImagePlugin.PngImageFile]
    google_tag_manager: Optional[str]
    language: Optional[str]
    territory: Optional[str]
    domain: Optional[str]
    text_dir: Optional[str]
    title: Optional[str]
    description: Optional[str]
    subject: Optional[str]
    main_color: Optional[str]
    background_color: Optional[str]
    author_name: Optional[str]
    author_email: Optional[str]
    facebook_app_id: Optional[str]
    twitter_username: Optional[str]
    twitter_user_id: Optional[str]
    itunes_app_id: Optional[str]
    itunes_affiliate_data: Optional[str]


class RequiredConfig(TypedDict):
    """
    The structure of the required part of the default config.
    """

    static_url: str


class ImagesConfig(TypedDict):
    """
    The structure of the images part of the default config.
    """

    favicon_ico: str
    favicon_png: str
    favicon_svg: str
    preview_png: str


class GeneralConfig(TypedDict):
    """
    The structure of the general part of the default config.
    """

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


class DefaultConfig(TypedDict):
    """
    The default config structure.
    """

    required: RequiredConfig
    images: ImagesConfig
    general: GeneralConfig


def get_default_config() -> DefaultConfig:
    """
    Generate the default config.

    Returns:
        a dict with the default config.
    """
    return {
        "required": {
            "static_url": "/static",
        },
        "images": {image.reference: f"./{image.name}" for image in helpers.get_assets_list()},
        "general": {
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
        },
    }


def validate_config(*, config: Config) -> NoReturn:
    """
    Validate a configuration.

    Args:
        config: the configuration.

    Raises:
        InvalidConfiguration: when the config isn't valid.
    """
    default_schema = schema.Schema({
        "required": {
            "static_url": str,
        },
        schema.Optional("images"): {
            schema.Optional("favicon_ico"): str,
            schema.Optional("favicon_png"): str,
            schema.Optional("favicon_svg"): str,
            schema.Optional("preview_png"): str,
        },
        schema.Optional("general"): {
            schema.Optional("google_tag_manager"): str,
            schema.Optional("language"): str,
            schema.Optional("territory"): str,
            schema.Optional("domain"): str,
            schema.Optional("text_dir"): str,
            schema.Optional("title"): str,
            schema.Optional("description"): str,
            schema.Optional("subject"): str,
            schema.Optional("main_color"): str,
            schema.Optional("background_color"): str,
            schema.Optional("author_name"): str,
            schema.Optional("author_email"): str,
            schema.Optional("facebook_app_id"): str,
            schema.Optional("twitter_username"): str,
            schema.Optional("twitter_user_id"): str,
            schema.Optional("itunes_app_id"): str,
            schema.Optional("itunes_affiliate_data"): str,
        },
    })
    try:
        default_schema.validate(config)
    except (
            schema.SchemaWrongKeyError,
            schema.SchemaMissingKeyError,
            schema.SchemaError,
    ) as exception:
        raise exceptions.InvalidConfiguration(exception)

    if config.get("general"):
        hex_color = re.compile('^#(?:[0-9a-fA-F]{3}){1,2}$')
        for color_key in ("main_color", "background_color"):
            if config["general"].get(color_key) and not hex_color.match(config["main_color"]):
                raise exceptions.InvalidConfiguration(f"The key {color_key} must be a hex color code")


def load_binary_image(*, path: str, expected_format: str) -> Union[IcoImagePlugin.IcoImageFile, PngImagePlugin.PngImageFile]:
    """
    Load a binary type image.

    Args:
        path: the image path
        expected_format: the expected format of the image.

    Returns:
        The image instance.

    Raises:
        BadReference: when the reference to the image isn't a file.
        WrongFileFormat: when the image isn't valid.
    """
    try:
        image = Image.open(path)
    except IsADirectoryError as exception:
        raise exceptions.BadReference("".join((
            "Image reference must be a file, not a directory",
            f"ABSOLUTE PATH: {path.absolute()}",
            f"Exception: {exception}",
        )))
    except Image.UnidentifiedImageError as exception:
        raise exceptions.WrongFileFormat("".join((
            "Can't identify image file",
            f"ABSOLUTE PATH: {path.absolute()}",
            f"Exception: {exception}",
        )))
    if image.format != expected_format:
        raise exceptions.WrongFileFormat("".join((
            f"Wrong image format. Expected {expected_format}, received {image.format}",
            f"ABSOLUTE PATH: {path.absolute()}",
        )))

    # Verify the image. After this, need to close it.
    image.verify()
    image.close()

    return Image.open(path)


def parse_config(*, path: str, config: dict) -> Config:
    """
    Parse a config.

    Args:
        path: config folder path.
        config: the config.

    Returns:
        A new dict with the parsed config.
    """
    parsed_config = {
        "main_folder_path": path,
        "output_folder_path": path / "output",

        # required
        **config["required"],

        # images
        'favicon_ico': '',
        'favicon_png': '',
        'favicon_svg': '',
        'preview_png': '',

        # general
        'google_tag_manager': '',
        'language': '',
        'territory': '',
        'domain': '',
        'text_dir': '',
        'title': '',
        'description': '',
        'subject': '',
        'main_color': '',
        'background_color': '',
        'author_name': '',
        'author_email': '',
        'facebook_app_id': '',
        'twitter_username': '',
        'twitter_user_id': '',
        'itunes_app_id': '',
        'itunes_affiliate_data': '',
    }
    if "images" in config:
        if "favicon_ico" in config["images"]:
            parsed_config["favicon_ico"] = load_binary_image(path=parsed_config["main_folder_path"] / config["images"]["favicon_ico"], expected_format='ICO')
        if "favicon_png" in config["images"]:
            parsed_config["favicon_png"] = load_binary_image(path=parsed_config["main_folder_path"] / config["images"]["favicon_png"], expected_format='PNG')
        if "favicon_svg" in config["images"]:
            parsed_config["favicon_svg"] = parsed_config["main_folder_path"] / config["images"]["favicon_svg"]
        if "preview_png" in config["images"]:
            parsed_config["preview_png"] = load_binary_image(path=parsed_config["main_folder_path"] / config["images"]["preview_png"], expected_format='PNG')
    parsed_config.update(**config.get("general"))
    return parsed_config
