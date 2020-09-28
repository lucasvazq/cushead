#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc
"""
import json
import pathlib
from src import helpers
import textwrap

import schema
from PIL import Image

from src import info
from src.console import console
from json import decoder


def read_config_file(*, path: str):
    """
    doc
    """
    with open(path, "r") as file:
        file_string = file.read()
    try:
        config = json.loads(file_string)
    except decoder.JSONDecodeError:
        raise console.MainException(textwrap.dedent(f"""\
            Invalid json file format in ({path})
            ABSOLUTE PATH: {path.absolute()}
        """))

    output_folder_path = pathlib.Path(path).parent
    return parse_config(path=output_folder_path, config=config)


def load_binary_image(*, path: str, expected_format: str):
    """
    doc
    """
    try:
        image = Image.open(path)
    except IsADirectoryError:
        raise console.MainException(textwrap.dedent(f"""\
            Image reference must be a file, not a directory
            ABSOLUTE PATH: {path.absolute()}
        """))
    except Image.UnidentifiedImageError:
        raise console.MainException(textwrap.dedent(f"""\
            Can't identify image file
            ABSOLUTE PATH: {path.absolute()}
        """))
    if image.format != expected_format:
        raise console.MainException(textwrap.dedent(f"""\
            Wrong image format. Expected {expected_format}, received {image.format}
            ABSOLUTE PATH: {path.absolute()}
        """))
    image.verify()
    image.close()

    # return a new instance of the image
    return Image.open(path)


def parse_config(*, path: str, config: dict) -> dict:
    """
    doc
    """

    # Construct config
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
        raise console.MainException(exception)

    # Make paths
    # Define the main path as the passed throught -file argument
    output_folder_path = path / "output"
    custom_settings = dict(
        {
            "main_folder_path": path,
            "output_folder_path": output_folder_path,
        },
        **config["required"],
        **config.get("general", {}),
        **config.get("social_media", {}),
        **config.get("static_url", {}),
    )

    if "images" in config:
        if "favicon_ico" in config["images"]:
            custom_settings["favicon_ico"] = load_binary_image(path=custom_settings["main_folder_path"] / config["images"]["favicon_ico"], expected_format='ICO')
        if "favicon_png" in config["images"]:
            custom_settings["favicon_png"] = load_binary_image(path=custom_settings["main_folder_path"] / config["images"]["favicon_png"], expected_format='PNG')
        if "preview_png" in config["images"]:
            custom_settings["preview_png"] = load_binary_image(path=custom_settings["main_folder_path"] / config["images"]["preview_png"], expected_format='PNG')
        if "favicon_svg" in config["images"]:
            custom_settings["favicon_svg"] = custom_settings["main_folder_path"] / config["images"]["favicon_svg"]

    return custom_settings


def default_settings() -> str:
    """
    Generate config file in indented JSON format
    """
    package_info = info.get_info()
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
            "author_name": package_info.author,
            "author_email": package_info.email,
        },
        "social_media": {
            "facebook_app_id": "123456",
            "twitter_username": "Microsoft",
            "twitter_user_id": "123456",
            "itunes_app_id": "123456",
            "itunes_affiliate_data": "123456",
        },
    }
