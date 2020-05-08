#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to handle the images configurations

Classes:
    IconsFormatConfigStructure
    IconsFormatConfig
"""
import os
import textwrap
import typing

import schema

import src.base.logs
import src.helpers
import src.info


def generate_default_config(output_path):
    pass


class FileAttributes:
    """Class to handle the a file objects attribute

    Init:
        file_name str = ''
        size Union[list, None] = None
    """

    def __init__(
        self,
        file_name: str = "",
        size: typing.Union[typing.List[int], None] = None,
    ):
        self.file_name = file_name
        self.size = size or []


class ImageFormater:
    """Class to define attributes of a png image

    Init:
        output_file_name str = ''
        output_file_size_verbosity bool = False
        output_folder_path str = ''
        source_file_path str = ''
        background_color str = ''
        sizes_max_min: Union[List[int], None] = None
        sizes_square: Union[List[int], None] = None
        sizes_rectangular: Union[List[int], None] = None
        sizes_mantain: bool = False
        head_output: bool = False
        url_path: str = ''
        tag_name: str = ''
        attribute_color: str = ''
        attribute_content: str = ''
        attribute_name: str = ''
        attribute_property: str = ''
        attribute_rel: str = ''
        attribute_type: str = ''
        attribute_special_content: bool = False
        attribute_special_href: bool = False
        attribute_special_sizes: bool = False
        attribute_special_title: bool = False
    """

    def __init__(
        self,
        output_file_name: str = "",
        output_file_size_verbosity: bool = False,
        output_folder_path: str = "",
        source_file_path: str = "",
        background_color: str = "",
        sizes_max_min: typing.Union[typing.List[int], None] = None,
        sizes_square: typing.Union[typing.List[int], None] = None,
        sizes_rectangular: typing.Union[typing.List[int], None] = None,
        sizes_mantain: bool = False,
        head_output: bool = False,
        url_path: str = "",
        tag_name: str = "",
        attribute_color: str = "",
        attribute_content: str = "",
        attribute_name: str = "",
        attribute_property: str = "",
        attribute_rel: str = "",
        attribute_type: str = "",
        attribute_special_content: bool = False,
        attribute_special_href: bool = False,
        attribute_special_sizes: bool = False,
        attribute_special_title: bool = False,
    ):
        self.ext = ".png"
        # output file name
        self.output_file_name = output_file_name
        self.output_file_size_verbosity = output_file_size_verbosity
        self.output_folder_path = output_folder_path
        # source
        self.source_file_path = source_file_path
        # background color
        self.background_color = background_color
        # sizes
        self.sizes_max_min = sizes_max_min or []
        self.sizes_square = sizes_square or []
        self.sizes_rectangular = sizes_rectangular or []
        self.sizes_mantain = sizes_mantain

        # head elements

        # general
        self.head_output = head_output
        self.url_path = url_path
        self.tag_name = tag_name
        # normal attributes
        self.attribute_color = attribute_color
        self.attribute_content = attribute_content
        self.attribute_name = attribute_name
        self.attribute_property = attribute_property
        self.attribute_rel = attribute_rel
        self.attribute_type = attribute_type
        # special attributes
        self.attribute_special_content = attribute_special_content
        self.attribute_special_href = attribute_special_href
        self.attribute_special_sizes = attribute_special_sizes
        self.attribute_special_title = attribute_special_title

        self.output_extension = os.path.splitext(self.source_file_path)[1]
        self.formated = self._output_formater()

    def _get_sizes(self) -> list:
        return (
            [[size, size] for size in self.sizes_square]
            + self.sizes_rectangular
            + self.sizes_max_min
        )

    def _output_formater(self) -> typing.List[FileAttributes]:
        """Return file name, sizes, dest, source resize"""
        output_file_names = []
        if self.sizes_mantain:
            file_nam = self.output_file_name + self.output_extension
            output_file_names.append(FileAttributes(file_name=file_nam))
        elif self.output_file_size_verbosity:
            output_file_name = self.output_file_name
            for size in self._get_sizes():
                file_nam = f"{output_file_name}-{size[0]}x{size[1]}"
                file_nam += self.output_extension
                output_file_names.append(
                    FileAttributes(file_name=file_nam, size=size)
                )
        else:
            # Probably it is only one, but with _get_sizes we get the size
            # wherever they come from: square_sizes, max_min or rectangular
            for size in self._get_sizes():
                output_file_names.append(
                    FileAttributes(
                        file_name=self.output_file_name
                        + self.output_extension,
                        size=size,
                    )
                )
        return output_file_names


class IconsFormatConfig:
    """Class to handle the default icons format configuration

    Methods:
        default_icons_config
    """

    def __init__(self, config):
        self.config = config
        self.image_format_config_dict = self._image_format_config()
        self.icons_config = self.get_icons_config()

    def _favicon_ico_icons_config(self) -> typing.List[ImageFormater]:
        if "favicon_ico" in self.image_format_config_dict:
            return [self.image_format_config_dict["favicon_ico"]]
        return []

    def _favicon_png_icons_config(self) -> typing.List[ImageFormater]:

        # Order matters for those icons
        ordered_icons = [
            self.image_format_config_dict.get("favicon_png"),
            self.image_format_config_dict.get("apple_touch_icon_default"),
            self.image_format_config_dict.get("apple_touch_icon"),
            self.image_format_config_dict.get("apple_touch_startup_image"),
            self.image_format_config_dict.get(
                "apple_touch_startup_image_media_queries"
            ),
            self.image_format_config_dict.get("yandex"),
        ]
        return [
            icon
            for icon in [
                *ordered_icons,
                self.image_format_config_dict.get("ms_icon"),
            ]
            if icon
        ]

    def _favicon_svg_icons_config(self) -> typing.List[ImageFormater]:
        if "mask_icon" in self.image_format_config_dict:
            return [self.image_format_config_dict["mask_icon"]]
        return []

    def _preview_png_icons_config(self) -> typing.List[ImageFormater]:
        return [
            icon
            for icon in [
                self.image_format_config_dict.get("preview_og"),
                self.image_format_config_dict.get("preview_og_secure_url"),
                self.image_format_config_dict.get("preview_twitter"),
            ]
            if icon
        ]

    def _browserconfig_icons_config(self) -> typing.List[ImageFormater]:
        if "browserconfig" in self.image_format_config_dict:
            return [self.image_format_config_dict["browserconfig"]]
        return []

    def _manifest_icons_config(self) -> typing.List[ImageFormater]:
        if "manifest" in self.image_format_config_dict:
            return [self.image_format_config_dict["manifest"]]
        return []

    def _opensearch_icons_config(self) -> typing.List[ImageFormater]:
        if "opensearch" in self.image_format_config_dict:
            return [self.image_format_config_dict["opensearch"]]
        return []

    def _image_format_config(self) -> dict:
        """Dictionary preloaded with custom data"""
        dictionary = {}

        if "favicon_ico" in self.config:
            dictionary["favicon_ico"] = ImageFormater(
                output_file_name="favicon",
                output_folder_path=self.config["output_folder_path"],
                source_file_path=self.config["favicon_ico"],
                sizes_mantain=True,
                head_output=True,
                url_path="/",
                tag_name="link",
                attribute_rel="icon",
                attribute_type="image/x-icon",
                attribute_special_href=True,
            )

        if "favicon_png" in self.config:
            dictionary.update(
                {
                    "favicon_png": ImageFormater(
                        output_file_name="favicon",
                        output_file_size_verbosity=True,
                        output_folder_path=self.config["static_folder_path"],
                        source_file_path=self.config["favicon_png"],
                        sizes_square=[16, 32, 96, 192, 194],
                        head_output=True,
                        url_path=self.config["static_url"],
                        tag_name="link",
                        attribute_rel="icon",
                        attribute_type="image/png",
                        attribute_special_sizes=True,
                        attribute_special_href=True,
                    ),
                    "ms_icon":
                    # LISTO
                    ImageFormater(
                        output_file_name="ms-icon",
                        output_file_size_verbosity=True,
                        output_folder_path=self.config["static_folder_path"],
                        source_file_path=self.config["favicon_png"],
                        sizes_square=[144],
                        head_output=True,
                        url_path=self.config["static_url"],
                        tag_name="meta",
                        attribute_name="msapplication-TileImage",
                        attribute_special_content=True,
                    ),
                    "apple_touch_icon_default": ImageFormater(
                        output_file_name="apple-touch-icon",
                        output_file_size_verbosity=True,
                        output_folder_path=self.config["static_folder_path"],
                        source_file_path=self.config["favicon_png"],
                        sizes_square=[57],
                        head_output=True,
                        url_path=self.config["static_url"],
                        tag_name="link",
                        attribute_rel="apple-touch-icon",
                        attribute_special_href=True,
                    ),
                    "apple_touch_icon": ImageFormater(
                        output_file_name="apple-touch-icon",
                        output_file_size_verbosity=True,
                        output_folder_path=self.config["static_folder_path"],
                        source_file_path=self.config["favicon_png"],
                        sizes_square=[
                            57,
                            60,
                            72,
                            76,
                            114,
                            120,
                            128,
                            144,
                            152,
                            167,
                            180,
                            195,
                            196,
                            228,
                            512,
                            1024,
                        ],
                        head_output=True,
                        url_path=self.config["static_url"],
                        tag_name="link",
                        attribute_rel="apple-touch-icon",
                        attribute_special_href=True,
                        attribute_special_sizes=True,
                    ),
                    "browserconfig":
                    # LISTO
                    ImageFormater(
                        output_file_name="browserconfig",
                        output_file_size_verbosity=True,
                        output_folder_path=self.config["static_folder_path"],
                        source_file_path=self.config["favicon_png"],
                        sizes_square=[30, 44, 70, 150, 310],
                        sizes_rectangular=[[310, 150]],
                    ),
                    "manifest":
                    # LISTO
                    ImageFormater(
                        output_file_name="manifest",
                        output_file_size_verbosity=True,
                        output_folder_path=self.config["static_folder_path"],
                        source_file_path=self.config["favicon_png"],
                        sizes_square=[192, 512],
                        attribute_type="image/png",
                    ),
                    "opensearch":
                    # LISTO
                    ImageFormater(
                        output_file_name="opensearch",
                        output_file_size_verbosity=True,
                        output_folder_path=self.config["static_folder_path"],
                        source_file_path=self.config["favicon_png"],
                        sizes_square=[16],
                        attribute_type="image/png",
                    ),
                }
            )
            multiple_initial_data = {
                "yandex": {
                    "output_file_name": "yandex",
                    "output_folder_path": self.config["static_folder_path"],
                    "source_file_path": self.config["favicon_png"],
                    "sizes_square": [120],
                    "head_output": True,
                    "url_path": self.config["static_url"],
                    "tag_name": "meta",
                    "attribute_name": "yandex-tableau-widget",
                    "attribute_content": f"logo={self.config['static_url']}/yandex.png",
                },
                "apple_touch_startup_image": {
                    "output_file_name": "apple-touch-startup-image",
                    "output_file_size_verbosity": True,
                    "output_folder_path": self.config["static_folder_path"],
                    "source_file_path": self.config["favicon_png"],
                    "sizes_square": [1024],
                    "head_output": True,
                    "url_path": self.config["static_url"],
                    "tag_name": "link",
                    "attribute_rel": "apple-touch-startup-image",
                    "attribute_special_href": True,
                },
                "apple_touch_startup_image_media_queries": {
                    # LISTO
                    "output_file_name": "apple-touch-startup-image",
                    "output_file_size_verbosity": True,
                    "output_folder_path": self.config["static_folder_path"],
                    "source_file_path": self.config["favicon_png"],
                    "sizes_max_min": [
                        # Source: https://github.com/onderceylan/pwa-asset-generator
                        [2048, 2732, 2],
                        [2732, 2048, 2],
                        [1668, 2388, 2],
                        [2388, 1668, 2],
                        [1668, 2224, 2],
                        [2224, 1668, 2],
                        [1536, 2048, 2],
                        [2048, 1536, 2],
                        [1242, 2688, 3],
                        [2688, 1242, 3],
                        [1125, 2436, 3],
                        [2436, 1125, 3],
                        [828, 1792, 2],
                        [1792, 828, 2],
                        [1242, 2208, 3],
                        [2208, 1242, 3],
                        [750, 1334, 2],
                        [1334, 750, 2],
                        [640, 1136, 2],
                        [1136, 640, 2],
                    ],
                    "head_output": True,
                    "url_path": self.config["static_url"],
                    "tag_name": "link",
                    "attribute_rel": "apple-touch-startup-image",
                    "attribute_special_href": True,
                },
            }
            if "background_color" in self.config:
                multiple_initial_data["yandex"][
                    "attribute_content"
                ] += f", color={self.config['background_color']}"
                multiple_initial_data["apple_touch_startup_image"][
                    "background_color"
                ] = self.config["background_color"]
                multiple_initial_data[
                    "apple_touch_startup_image_media_queries"
                ]["background_color"] = self.config["background_color"]
            dictionary["yandex"] = ImageFormater(
                **multiple_initial_data["yandex"]
            )
            dictionary["apple_touch_startup_image"] = ImageFormater(
                **multiple_initial_data[
                    "apple_touch_startup_image_media_queries"
                ]
            )
            dictionary[
                "apple_touch_startup_image_media_queries"
            ] = ImageFormater(
                **multiple_initial_data[
                    "apple_touch_startup_image_media_queries"
                ]
            )

        # LISTO
        if "favicon_svg" in self.config:
            initial_data = {
                "output_file_name": "mask-icon",
                "output_folder_path": self.config["static_folder_path"],
                "source_file_path": self.config["favicon_svg"],
                "sizes_mantain": True,
                "head_output": True,
                "url_path": self.config["static_url"],
                "tag_name": "link",
                "attribute_rel": "mask-icon",
                "attribute_special_href": True,
            }
            if "main_color" in self.config:
                initial_data["attribute_color"] = self.config["main_color"]
            dictionary["mask_icon"] = ImageFormater(**initial_data)

        if "preview_png" in self.config:
            dictionary.update(
                {
                    # LISTO
                    "preview_og": ImageFormater(
                        output_file_name="preview",
                        output_folder_path=self.config["static_folder_path"],
                        output_file_size_verbosity=True,
                        source_file_path=self.config["preview_png"],
                        sizes_square=[600, 1080],
                        head_output=True,
                        url_path=self.config["static_url"],
                        tag_name="meta",
                        attribute_property="og:image",
                        attribute_special_content=True,
                    ),
                    # LISTO
                    "preview_twitter": ImageFormater(
                        output_file_name="preview",
                        output_folder_path=self.config["static_folder_path"],
                        output_file_size_verbosity=True,
                        source_file_path=self.config["preview_png"],
                        sizes_square=[600],
                        head_output=True,
                        url_path=self.config["static_url"],
                        tag_name="meta",
                        attribute_name="twitter:image",
                        attribute_special_content=True,
                    ),
                }
            )

        return dictionary

    def get_icons_config(self) -> typing.Dict[str, typing.List[ImageFormater]]:
        """Return a default icons format configuration

        This return includes configs for favicons with png extension and for
        browserconfig, manifest and opensearch related icons
        """
        return self._image_format_config()


def default_images() -> typing.List[typing.Dict[str, str]]:
    """Generate images files to attach to the preset settings"""
    binary_files = []
    realpath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "../assets"
    )
    image_files = src.helpers.images_list()
    for filename in image_files:
        filepath = os.path.join(realpath, filename)
        with open(filepath, "rb") as binary_file:
            binary_files.append(
                {"filename": filename, "content": binary_file.read()}
            )
    return binary_files


class UserConfigHandler(src.base.logs.Logs):
    def transform(
        self, settings: typing.Union[dict, None] = None, main_path: str = ""
    ) -> dict:
        """Format default settings to a dict for this package classes

        Format default settings dictionary into a dictionary that the classes
        under this package can understand

        Args:
            settings dict: Pass a default settings dict format
            main_path: base path folder

        Returns:
            dict: config that the classes under this module can use

        """

        # Construct config
        default_schema = schema.Schema(
            {
                schema.Optional("comment"): dict,
                "configuration": {
                    "required": {"static_url": str},
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
                },
            }
        )

        try:
            default_schema.validate(settings)
        except (
            schema.SchemaWrongKeyError,
            schema.SchemaMissingKeyError,
            schema.SchemaError,
        ) as exception:
            self.error_log(exception)

        # Make paths
        # Define the main path as the passed throught -file argument
        output_folder_path = os.path.join(main_path, "output")
        static_folder_path = os.path.join(output_folder_path, "static")
        custom_settings = dict(
            {
                "main_folder_path": main_path,
                "output_folder_path": output_folder_path,
                "static_folder_path": static_folder_path,
            },
            **settings["configuration"]["required"],
            **settings["configuration"].get("general", {}),
            **settings["configuration"].get("social_media", {}),
            **settings["configuration"].get("static_url", {}),
        )

        if "images" in settings["configuration"]:
            if "favicon_ico" in settings["configuration"]["images"]:
                custom_settings["favicon_ico"] = os.path.join(
                    custom_settings["main_folder_path"],
                    settings["configuration"]["images"]["favicon_ico"],
                )
            if "favicon_png" in settings["configuration"]["images"]:
                custom_settings["favicon_png"] = os.path.join(
                    custom_settings["main_folder_path"],
                    settings["configuration"]["images"]["favicon_png"],
                )
            if "favicon_svg" in settings["configuration"]["images"]:
                custom_settings["favicon_svg"] = os.path.join(
                    custom_settings["main_folder_path"],
                    settings["configuration"]["images"]["favicon_svg"],
                )
            if "preview_png" in settings["configuration"]["images"]:
                custom_settings["preview_png"] = os.path.join(
                    custom_settings["main_folder_path"],
                    settings["configuration"]["images"]["preview_png"],
                )

        return custom_settings


def default_settings() -> str:
    """Generate config file in indented JSON format"""

    info = src.info.get_info()

    settings = textwrap.dedent(
        f"""\
        {{
            'comment':  {{
                'About': 'Config file used by python CUSHEAD',
                'Format': 'JSON',
                'Git': '{info['source']}',
                'Documentation': '{info['documentation']}'
            }},
            'configuration': {{
                'required': {{
                    'static_url': '/static'
                }},
                'images': {{
                    'favicon_ico': './favicon_ico_16px.ico',
                    'favicon_png': './favicon_png_1600px.png',
                    'favicon_svg': './favicon_svg_scalable.svg',
                    'preview_png': './preview_png_500px.png'
                }},
                'general': {{
                    'google_tag_manager': 'GTM-*******',
                    'language': 'en',
                    'territory': 'US',
                    'domain': 'microsoft.com',
                    'text_dir': 'ltr',
                    'title': 'Microsoft',
                    'description': 'Technology Solutions',
                    'subject': 'Home Page',
                    'main_color': '#ff0000',
                    'background_color': '#ffffff',
                    'author_name': '{info['author']}',
                    'author_email': '{info['email']}'
                }},
                'social_media': {{
                    'facebook_app_id': '123456',
                    'twitter_username':'Microsoft',
                    'twitter_user_id': '123456',
                    'itunes_app_id': '123456',
                    'itunes_affiliate_data': '123456'
                }}
            }}
        }}"""
    )
    settings = settings.replace("'", '"')
    return settings
