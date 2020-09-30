#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc
"""
import json
import pathlib
from json import decoder
from typing import TypedDict
from typing import Optional
from typing import NoReturn

import schema
from PIL import IcoImagePlugin
from PIL import Image
from PIL import PngImagePlugin

from src import exceptions
from src import helpers
from src import info


def read_config_file(*, path: str):
    """
    doc
    """
    with open(path, "r") as file:
        file_string = file.read()
    try:
        config = json.loads(file_string)
    except decoder.JSONDecodeError as exception:
        raise exceptions.MainException("".join((
            f"Invalid json file format in ({path})",
            f"ABSOLUTE PATH: {path.absolute()}",
            f"Exception: {exception}"
        )))

    output_folder_path = pathlib.Path(path).parent
    return parse_config(path=output_folder_path, config=config)


def load_binary_image(*, path: str, expected_format: str):
    """
    doc
    """
    try:
        image = Image.open(path)
    except IsADirectoryError as exception:
        raise exceptions.MainException("".join((
            "Image reference must be a file, not a directory",
            f"ABSOLUTE PATH: {path.absolute()}",
            f"Exception: {exception}",
        )))
    except Image.UnidentifiedImageError as exception:
        raise exceptions.MainException("".join((
            "Can't identify image file",
            f"ABSOLUTE PATH: {path.absolute()}",
            f"Exception: {exception}",
        )))
    if image.format != expected_format:
        raise exceptions.MainException("".join((
            f"Wrong image format. Expected {expected_format}, received {image.format}",
            f"ABSOLUTE PATH: {path.absolute()}",
        )))
    image.verify()
    image.close()

    # return a new instance of the image
    return Image.open(path)


class Config(TypedDict):
    """
    doc
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


def validate_config(*, config: dict) -> NoReturn:
    """
    doc
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
        },
        schema.Optional("social_media"): {
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
        raise exceptions.MainException(exception)


def parse_config(*, path: str, config: dict) -> Config:
    """
    doc
    """

    validate_config(config=config)

    parsed_config = {
        "main_folder_path": path,
        "output_folder_path": path / "output",
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

        # social_media
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
    parsed_config.update(
        **config.get("general", {}),
        **config.get("social_media", {}),
    )

    return parsed_config


def default_settings() -> str:
    """
    doc
    """
    return {
        "required": {
            "static_url": "/static",
        },
        "images": {image.reference: f"./{image.name}" for image in helpers.get_images_list()},
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
        },
        "social_media": {
            "facebook_app_id": "123456",
            "twitter_username": "Microsoft",
            "twitter_user_id": "123456",
            "itunes_app_id": "123456",
            "itunes_affiliate_data": "123456",
        },
    }
