"""
Handle the config.
"""
import pathlib
import re
from typing import Any
from typing import Literal
from typing import Optional
from typing import TypedDict
from typing import Union
from typing import overload

import schema
from PIL import IcoImagePlugin
from PIL import Image
from PIL import PngImagePlugin

from cushead import exceptions


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


def validate_config(*, config: Any) -> None:
    """
    Validate a config.

    Args:
        config: the config.

    Raises:
        InvalidConfig: when the config isn't valid.
    """
    default_schema = schema.Schema(
        {
            "static_url": str,
            schema.Optional("favicon_ico"): schema.Or(None, str),
            schema.Optional("favicon_png"): schema.Or(None, str),
            schema.Optional("favicon_svg"): schema.Or(None, str),
            schema.Optional("preview_png"): schema.Or(None, str),
            schema.Optional("google_tag_manager"): schema.Or(None, str),
            schema.Optional("language"): schema.Or(None, str),
            schema.Optional("territory"): schema.Or(None, str),
            schema.Optional("domain"): schema.Or(None, str),
            schema.Optional("text_dir"): schema.Or(None, str),
            schema.Optional("title"): schema.Or(None, str),
            schema.Optional("description"): schema.Or(None, str),
            schema.Optional("subject"): schema.Or(None, str),
            schema.Optional("main_color"): schema.Or(None, str),
            schema.Optional("background_color"): schema.Or(None, str),
            schema.Optional("author_name"): schema.Or(None, str),
            schema.Optional("author_email"): schema.Or(None, str),
            schema.Optional("facebook_app_id"): schema.Or(None, str),
            schema.Optional("twitter_username"): schema.Or(None, str),
            schema.Optional("twitter_user_id"): schema.Or(None, str),
            schema.Optional("itunes_app_id"): schema.Or(None, str),
            schema.Optional("itunes_affiliate_data"): schema.Or(None, str),
        }
    )
    try:
        default_schema.validate(config)
    except (
        schema.SchemaWrongKeyError,
        schema.SchemaMissingKeyError,
        schema.SchemaError,
    ) as exception:
        raise exceptions.InvalidConfig(exception)

    if not re.match("^((https?://|/).*)?$", config["static_url"]):
        raise exceptions.InvalidConfig("The key static_url must starts with a slash, http://, https:// or be an empty string.")
    if config["static_url"].endswith("/"):
        raise exceptions.InvalidConfig("The key static_url can't end with a slash.")

    hex_color = re.compile("^#(?:[0-9A-Fa-f]{3}){1,2}$")
    for color_key in ("main_color", "background_color"):
        if config.get(color_key) and not hex_color.match(config[color_key]):
            raise exceptions.InvalidConfig(f"The key {color_key} must be a hex color code. If you don't want any value on this key, set the value to null.")


@overload
def load_binary_image(*, key: Literal["favicon_ico"], path: pathlib.Path, expected_format: Literal["ICO"]) -> IcoImagePlugin.IcoImageFile:
    ...


@overload
def load_binary_image(*, key: Union[Literal["favicon_png"], Literal["preview_png"]], path: pathlib.Path, expected_format: Literal["PNG"]) -> PngImagePlugin.PngImageFile:
    ...


def load_binary_image(*, key, path, expected_format):
    """
    Load a binary type image.

    Args:
        path: the image path.
        expected_format: the expected format of the image.

    Returns:
        The image instance.

    Raises:
        BadReference: when the reference to the image doesn't exist or isn't a file.
        WrongFileFormat: when the image isn't valid.
    """
    if not path.exists():
        raise exceptions.BadReference(
            "\n".join(
                (
                    f"{key} reference ({path}) doesn't exists.",
                    f"ABSOLUTE PATH: {path.absolute()}",
                ),
            ),
        )
    try:
        image = Image.open(path)
    except IsADirectoryError as exception:
        raise exceptions.BadReference(
            "\n".join(
                (
                    f"{key} reference ({path}) must be a file, not a directory.",
                    f"Exception: {exception}",  # It includes the absolute path
                ),
            ),
        )
    except Image.UnidentifiedImageError as exception:
        raise exceptions.WrongFileFormat(
            "\n".join(
                (
                    f"Can't identify as image the {key} reference ({path}).",
                    f"Exception: {exception}",  # It includes the absolute path
                ),
            ),
        )

    if image.format != expected_format:
        image.close()
        raise exceptions.WrongFileFormat(
            "\n".join(
                (
                    f"The {key} reference ({path}) has a wrong image format.",
                    f"Expected {expected_format}, but received {image.format}.",
                    f"ABSOLUTE PATH: {path.absolute()}",
                ),
            ),
        )

    # Verify the image. After this, need to close it.
    image.verify()
    image.close()

    return Image.open(path)


def parse_config(*, path: pathlib.Path, config: Any) -> Config:
    """
    Parse a config.

    Args:
        path: the config file source path.
        config: the config.

    Returns:
        A new dict with the parsed config.
    """
    if config.get("favicon_ico"):
        favicon_ico = load_binary_image(key="favicon_ico", path=path / config["favicon_ico"], expected_format="ICO")
    else:
        favicon_ico = None

    if config.get("favicon_png"):
        favicon_png = load_binary_image(key="favicon_png", path=path / config["favicon_png"], expected_format="PNG")
    else:
        favicon_png = None

    if config.get("favicon_svg"):
        favicon_svg = path / config["favicon_svg"]
    else:
        favicon_svg = None

    if config.get("preview_png"):
        preview_png = load_binary_image(key="preview_png", path=path / config["preview_png"], expected_format="PNG")
    else:
        preview_png = None

    return {
        "main_folder_path": path,
        "output_folder_path": path / "output",
        "static_url": str(config["static_url"]),
        "favicon_ico": favicon_ico,
        "favicon_png": favicon_png,
        "favicon_svg": favicon_svg,
        "preview_png": preview_png,
        "google_tag_manager": config.get("google_tag_manager"),
        "language": config.get("language"),
        "territory": config.get("territory"),
        "domain": config.get("domain"),
        "text_dir": config.get("text_dir"),
        "title": config.get("title"),
        "description": config.get("description"),
        "subject": config.get("subject"),
        "main_color": config.get("main_color"),
        "background_color": config.get("background_color"),
        "author_name": config.get("author_name"),
        "author_email": config.get("author_email"),
        "facebook_app_id": config.get("facebook_app_id"),
        "twitter_username": config.get("twitter_username"),
        "twitter_user_id": config.get("twitter_user_id"),
        "itunes_app_id": config.get("itunes_app_id"),
        "itunes_affiliate_data": config.get("itunes_affiliate_data"),
    }
