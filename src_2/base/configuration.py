#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to handle the images configurations

Classes:
    IconsFormatConfigStructure
    IconsFormatConfig
"""
import os

import typing
import textwrap

import src_2.helpers
import src_2.base.logs
import src_2.info


def generate_default_config(output_path):
    pass


class FileAttributes:
    """Class to handle the a file objects attribute

    Init:
        file_name str = ''
        size Union[list, None] = None
    """

    def __init__(self,
                 file_name: str = "",
                 size: typing.Union[typing.List[int], None] = None):
        self.file_name = file_name
        self.size = size or []


class ImageFormater:
    """Class to define attributes of a png image

    Init:
        output_file_name str = ''
        output_file_size_verbosity bool = False
        output_folder_path str = ''
        source_file_path str = ''
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
        # output file name
        self.output_file_name = output_file_name
        self.output_file_size_verbosity = output_file_size_verbosity
        self.output_folder_path = output_folder_path
        # source
        self.source_file_path = source_file_path
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
        sizes_square = [[size, size] for size in self.sizes_square]
        sizes_rectangular = self.sizes_rectangular
        sizes_max_min = [[size[1], size[1]] for size in self.sizes_max_min]
        return sizes_square + sizes_rectangular + sizes_max_min

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
                    FileAttributes(file_name=file_nam, size=size))
        else:
            # Probably it is only one, but with _get_sizes we get the size
            # wherever they come from: square_sizes, max_min or rectangular
            for size in self._get_sizes():
                output_file_names.append(
                    FileAttributes(
                        file_name=self.output_file_name +
                        self.output_extension,
                        size=size,
                    ))
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

        return [
            # <link rel='shortcut icon' href='/favicon.ico'
            # type='image/x-icon'>
            self.image_format_config_dict["favicon_ico"]
        ]

    def _favicon_png_icons_config(self) -> typing.List[ImageFormater]:

        # Order matters
        return [
            # Default png favicon
            # Example:
            # <link rel="icon" type="image/png" href="/static/favicon-16x16.png"
            # sizes="16x16">
            self.image_format_config_dict["favicon_16x16_png"],

            # Microsoft icon
            # Example:
            # <meta name="msapplication-TileImage"
            # content="/static/ms-icon-144x144.png">
            self.image_format_config_dict["ms_icon"],

            # Apple touch default
            # Example:
            # <link rel="apple-touch-icon"
            # href="/static/apple-touch-icon-default-57x57.png">
            self.image_format_config_dict["apple_touch_icon_default"],

            # Apple touch with different sizes
            # Example:
            # <link rel="apple-touch-icon" sizes="57x57"
            # href="/static/apple-touch-icon-57x57.png">
            self.image_format_config_dict["apple_touch_icon"],

            # Apple touch startup default
            # Example:
            # ???
            self.image_format_config_dict["apple_touch_startup_image"],

            # Apple touch startup with different sizes
            # Example:
            # ???
            self.image_format_config_dict[
                "apple_touch_startup_image_media_queries"],

            # Fluid icon
            # Example:
            # <link rel="fluid-icon" href="/static/fluidicon-512x512.png"
            # title="Microsoft">
            self.image_format_config_dict["fluid-icon"],

            # Yandex browser special icon
            # Example:
            # ???
            self.image_format_config_dict["yandex"],
        ]

    def _favicon_svg_icons_config(self) -> typing.List[ImageFormater]:
        return [
            # <link color="blue" rel="mask-icon" href="/static/favicon.svg"
            self.image_format_config_dict["mask-icon"]
        ]

    def _preview_png_icons_config(self) -> typing.List[ImageFormater]:
        return [
            # <meta property='og:image' content='/static/preview-500x500.png'>
            self.image_format_config_dict["preview_og"],
            # <meta property='og:image:secure_url'
            # content='/static/preview-500x500.png'>
            self.image_format_config_dict["preview_og_secure_url"],
            # <meta name='twitter:image' content='/static/preview-500x500.png'>
            self.image_format_config_dict["preview_twitter"],
        ]

    def _browserconfig_icons_config(self) -> typing.List[ImageFormater]:
        return [self.image_format_config_dict["browserconfig"]]

    def _manifest_icons_config(self) -> typing.List[ImageFormater]:
        return [self.image_format_config_dict["manifest"]]

    def _opensearch_icons_config(self) -> typing.List[ImageFormater]:
        return [self.image_format_config_dict["opensearch"]]

    def _image_format_config(self) -> dict:
        """Dictionary preloaded with custom data"""

        favicon_ico = self.config.get("favicon_ico", "")
        favicon_png = self.config.get("favicon_png", "")
        favicon_svg = self.config.get("favicon_svg", "")
        preview_png = self.config.get("preview_png", "")
        output_folder_path = self.config.get("output_folder_path", "")
        static_folder_path = self.config.get("static_folder_path", "")
        static_url = self.config.get("static_url", "")
        background_color = self.config.get("background_color", "")
        yandex_content = (f"logo={static_url}/yandex.png, "
                          f"color={background_color}")

        return {
            # favicon ico
            "favicon_ico":
            ImageFormater(
                output_file_name="favicon",
                output_folder_path=output_folder_path,
                source_file_path=favicon_ico,
                sizes_mantain=True,
                head_output=True,
                url_path="/",
                tag_name="link",
                attribute_rel="icon",
                attribute_type="image/x-icon",
                attribute_special_href=True,
            ),

            # favicon png
            "favicon_16x16_png":
            ImageFormater(
                output_file_name="favicon",
                output_file_size_verbosity=True,
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                # https://www.favicon-generator.org/
                # https://stackoverflow.com/questions/4014823/does-a-favicon-have-to-be-32x32-or-16x16
                # https://www.emergeinteractive.com/insights/detail/the-essentials-of-favicons/
                sizes_square=[
                    16,
                    24,
                    32,
                    48,
                    57,
                    60,
                    64,
                    70,
                    72,
                    76,
                    96,
                    114,
                    120,
                    128,
                    144,
                    150,
                    152,
                    167,
                    180,
                    192,
                    195,
                    196,
                    228,
                    310,
                ],
                head_output=True,
                url_path=static_url,
                tag_name="link",
                attribute_rel="icon",
                attribute_type="image/png",
                attribute_special_sizes=True,
                attribute_special_href=True,
            ),
            "ms_icon":
            ImageFormater(
                output_file_name="ms-icon",
                output_file_size_verbosity=True,
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[144],
                head_output=True,
                url_path=static_url,
                tag_name="meta",
                attribute_name="msapplication-TileImage",
                attribute_special_content=True,
            ),
            "apple_touch_icon_default":
            ImageFormater(
                output_file_name="apple-touch-icon",
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[57],
                head_output=True,
                url_path=static_url,
                tag_name="link",
                attribute_rel="apple-touch-icon",
                attribute_special_href=True,
            ),
            "apple_touch_icon":
            ImageFormater(
                output_file_name="apple-touch-icon",
                output_file_size_verbosity=True,
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[
                    57,
                    60,
                    72,
                    76,
                    114,
                    120,
                    144,
                    152,
                    167,
                    180,
                    1024,
                ],
                head_output=True,
                url_path=static_url,
                tag_name="link",
                attribute_rel="apple-touch-icon",
                attribute_special_href=True,
                attribute_special_sizes=True,
            ),
            "apple_touch_startup_image":
            ImageFormater(
                output_file_name="launch",
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[768],
                head_output=True,
                url_path=static_url,
                tag_name="link",
                attribute_rel="apple-touch-startup-image",
                attribute_special_href=True,
            ),
            "apple_touch_startup_image_media_queries":
            ImageFormater(
                output_file_name="launch",
                output_file_size_verbosity=True,
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                # Based in:
                # https://css-tricks.com/snippets/css/media-queries-for-standard-devices/
                sizes_max_min=[
                    [38, 42],
                    [320, 375],
                    [375, 414],
                    [414, 480],
                    [480, 568],
                    [568, 667],
                    [667, 736],
                    [736, 812],
                    [812, 834],
                    [1024, 1112],
                    [1112, 1200],
                    [1200, 1366],
                    [1366, 1600],
                ],
                head_output=True,
                url_path=static_url,
                tag_name="link",
                attribute_rel="apple-touch-startup-image",
                attribute_special_href=True,
            ),
            "fluid-icon":
            ImageFormater(
                output_file_name="fluid-icon",
                output_folder_path=static_folder_path,
                output_file_size_verbosity=True,
                source_file_path=favicon_png,
                sizes_square=[512],
                head_output=True,
                url_path=static_url,
                tag_name="link",
                attribute_rel="fluid-icon",
                attribute_special_href=True,
                attribute_special_title=True,
            ),
            "yandex":
            ImageFormater(
                output_file_name="yandex",
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[120],
                head_output=True,
                url_path=static_url,
                tag_name="meta",
                attribute_name="yandex-tableau-widget",
                attribute_content=yandex_content,
            ),

            # favicon svg
            "mask-icon":
            ImageFormater(
                output_file_name="mask-icon",
                output_folder_path=static_folder_path,
                source_file_path=favicon_svg,
                sizes_mantain=True,
                head_output=True,
                url_path=static_url,
                tag_name="link",
                attribute_color=background_color,
                attribute_rel="mask-icon",
                attribute_special_href=True,
            ),

            # preview png
            "preview_og":
            ImageFormater(
                output_file_name="preview",
                output_folder_path=static_folder_path,
                output_file_size_verbosity=True,
                source_file_path=preview_png,
                sizes_square=[500],
                head_output=True,
                url_path=static_url,
                tag_name="meta",
                attribute_property="og:image",
                attribute_special_content=True,
            ),
            "preview_og_secure_url":
            ImageFormater(
                output_file_name="preview",
                output_folder_path=static_folder_path,
                output_file_size_verbosity=True,
                source_file_path=preview_png,
                sizes_square=[500],
                head_output=True,
                url_path=static_url,
                tag_name="meta",
                attribute_property="og:image:secure_url",
                attribute_special_content=True,
            ),
            "preview_twitter":
            ImageFormater(
                output_file_name="preview",
                output_folder_path=static_folder_path,
                output_file_size_verbosity=True,
                source_file_path=preview_png,
                sizes_square=[500],
                head_output=True,
                url_path=static_url,
                tag_name="meta",
                attribute_name="twitter:image",
                attribute_special_content=True,
            ),

            # complementary files
            "browserconfig":
            ImageFormater(
                output_file_name="ms-icon",
                output_file_size_verbosity=True,
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[30, 44, 70, 150, 310],
                sizes_rectangular=[[310, 150]],
            ),
            "manifest":
            ImageFormater(
                output_file_name="android-icon",
                output_file_size_verbosity=True,
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[36, 48, 72, 96, 144, 192, 256, 384, 512],
                attribute_type="image/png",
            ),
            "opensearch":
            ImageFormater(
                output_file_name="opensearch",
                output_file_size_verbosity=True,
                output_folder_path=static_folder_path,
                source_file_path=favicon_png,
                sizes_square=[16],
                attribute_type="image/png",
            ),
        }

    def get_icons_config(self) -> typing.Dict[str, typing.List[ImageFormater]]:
        """Return a default icons format configuration

        This return includes configs for favicons with png extension and for
        browserconfig, manifest and opensearch related icons
        """
        return {
            "favicon_ico": self._favicon_ico_icons_config(),
            "favicon_png": self._favicon_png_icons_config(),
            "favicon_svg": self._favicon_svg_icons_config(),
            "preview_png": self._preview_png_icons_config(),
            "browserconfig": self._browserconfig_icons_config(),
            "manifest": self._manifest_icons_config(),
            "opensearch": self._opensearch_icons_config(),
        }


def default_images() -> typing.List[typing.Dict[str, str]]:
    """Generate images files to attach to the preset settings"""
    binary_files = []
    realpath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            "../assets")
    image_files = src_2.helpers.images_list()
    for filename in image_files:
        filepath = os.path.join(realpath, filename)
        with open(filepath, "rb") as binary_file:
            binary_files.append({
                "filename": filename,
                "content": binary_file.read()
            })
    return binary_files


class UserConfigHandler(src_2.base.logs.Logs):
    def transform(self,
                  settings: typing.Union[dict, None] = None,
                  main_path: str = "") -> dict:
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
        recommended = settings.get("recommended", {})
        default = settings.get("default", {})
        general = default.get("general", {})
        basic = default.get("basic", {})
        social_media = default.get("social_media", {})
        progressive_web_app = settings.get("progressive_web_apps", {})
        if "required" not in settings:
            self.error_log(
                "Miss 'required' object and it's required in config file.")
        settings = {
            **settings["required"],
            **recommended,
            **general,
            **basic,
            **social_media,
            **progressive_web_app,
        }

        # Required values
        required_values = ["static_url"]
        for key in required_values:
            if error := src_2.helpers.key_exists(key, settings):
                self.error_log(error)

        # Sanitize static_url key
        # Prevent:
        #   output = /output/
        #   static_url = /static/
        #   output + static_url = /static/ [root/static/]
        if settings["static_url"][0] == "/":
            settings["static_folder_path"] = settings["static_url"][1:]
        # Prevent //
        if settings["static_url"][-1] == "/":
            settings["static_url"] = settings["static_url"][:-1]
        # Static url = "static" , not "static/"

        # Make paths
        # Define the main path as the passed throught -file argument
        settings["main_folder_path"] = main_path
        settings["output_folder_path"] = os.path.join(
            settings["main_folder_path"], "output")
        settings["static_folder_path"] = os.path.join(
            settings["output_folder_path"], settings["static_folder_path"])

        settings["favicon_ico"] = os.path.join(settings["main_folder_path"],
                                               settings["favicon_ico"])
        settings["favicon_png"] = os.path.join(settings["main_folder_path"],
                                               settings["favicon_png"])
        settings["favicon_svg"] = os.path.join(settings["main_folder_path"],
                                               settings["favicon_svg"])
        settings["preview_png"] = os.path.join(settings["main_folder_path"],
                                               settings["preview_png"])
        return settings


def default_settings() -> str:
    """Generate config file in indented JSON format"""

    info = src_2.info.Info.get_info()

    settings = textwrap.dedent(f"""\
        {{
            'comment':  {{
                'About':            'Config file used by python CUSHEAD',
                'Format':           'JSON',
                'Git':              '{info['source']}',
                'Documentation':    '{info['documentation']}'
            }},
            'required': {{
                'static_url':       '/static/'
            }},
            'recommended': {{
                'favicon_ico':      './favicon_ico_16px.ico',
                'favicon_png':      './favicon_png_1600px.png',
                'favicon_svg':      './favicon_svg_scalable.svg',
                'preview_png':      './preview_png_500px.png'
            }},
            'default': {{
                'general': {{
                    'content-type':     'text/html; charset=utf-8',
                    'X-UA-Compatible':  'ie=edge',
                    'viewport':         '{('width=device-width, '
                                           'initial-scale=1')}',
                    'language':         'en',
                    'territory':        'US',
                    'protocol':         'https://',
                    'clean_url':        'microsoft.com',
                    'robots':           'index, follow'
                }},
                'basic': {{
                    'title':            'Microsoft',
                    'description':      'Technology Solutions',
                    'subject':          'Home Page',
                    'keywords':         'Microsoft, Windows',
                    'background_color': '#FFFFFF',
                    'author':           'Lucas Vazquez'
                }},
                'social_media': {{
                    'facebook_app_id':  '123456',
                    'twitter_user_@':   '@Microsoft',
                    'twitter_user_id':  '123456'
                }}
            }},
            'progressive_web_apps': {{
                'dir':              'ltr',
                'start_url':        '/',
                'orientation':      'landscape',
                'scope':            '/',
                'display':          'browser',
                'platform':         'web'
            }}
        }}""")
    settings = settings.replace("'", '"')
    return settings
