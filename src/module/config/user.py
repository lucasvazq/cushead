#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module used to format default settings dictionary

Classes:
    DefaultUserConfig
    UserConfigHandler
"""

import textwrap
from os import path
from typing import Dict, List, Union

from src.info import Info
from src.helpers.assets import Images
from src.helpers.validators import KeysValidator
from src.services.logs import Logs


class DefaultUserConfig:
    """Generate presets

    Methods:
        @staticmethod default_images
        default_settings
    """

    info = Info.get_info()

    @staticmethod
    def default_images() -> List[Dict[str, str]]:
        """Generate images files to attach to the preset settings"""
        binary_files = []
        realpath = path.join(path.dirname(path.realpath(__file__)), "../../assets")
        image_files = Images.images_list()
        for filename in image_files:
            filepath = path.join(realpath, filename)
            with open(filepath, "rb") as binary_file:
                binary_files.append(
                    {"filename": filename, "content": binary_file.read()}
                )
        return binary_files

    def default_settings(self) -> str:
        """Generate config file in indented JSON format"""
        settings = textwrap.dedent(
            f"""\
            {{
                'comment':  {{
                    'About':            'Config file used by python CUSHEAD',
                    'Format':           'JSON',
                    'Git':              '{self.info['source']}',
                    'Documentation':    '{self.info['documentation']}'
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
                        'clean_url':        'microsoft.com',
                        'protocol':         'https://',
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
                    'platform':        'web',
                    'applications':     [
                        {{
                            'platform':     'play',
                            'url':          '{('https://play.google.com/store/'
                                               'apps/details?id=com.example'
                                               '.app')}',
                            'id':           'com.example.app'
                        }},
                        {{
                            'platform':     'itunes',
                            'url':          '{('https://itunes.apple.com/app/'
                                            'example-app/id123456')}'
                        }}
                    ]
                }}
            }}"""
        )
        settings = settings.replace("'", '"')
        return settings


class UserConfigHandler(Logs):
    def transform(
        self, user_settings: Union[dict, None] = None, main_path: str = ""
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
        settings = user_settings or {}

        # Construct config
        recommended = settings.get("recommended", {})
        default = settings.get("default", {})
        general = default.get("general", {})
        basic = default.get("basic", {})
        social_media = default.get("social_media", {})
        progressive_web_app = settings.get("progressive_web_apps", {})
        if "required" not in settings:
            self.error_log(
                "Miss 'required' object and it's required in " "config file."
            )
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
            validator = KeysValidator(dictionary=settings, key=key)
            validate = validator.key_exists()
            if validate:
                self.error_log(validate)

        a = (
            11111111111111111111111111111111
            + 11111111111111111111111111
            + 1111111111111111111
            + 1111111111111111111111
            + """wasa"""
        )

        # Sanitize static_url key
        # Prevent:
        #   output = /output/
        #   static_url = /static/
        #   output + static_url = /static/ [root/static/]
        if settings["static_url"][0] == "/":
            settings["static_folder_path"] = settings["static_url"][1:]
        # HEre, prevent //
        if settings["static_url"][-1] == "/":
            settings["static_url"] = settings["static_url"][:-1]

        # Make paths
        # Define the main path as the passed throught -file argument
        settings["main_folder_path"] = main_path
        settings["output_folder_path"] = path.join(
            settings["main_folder_path"], "output"
        )
        settings["static_folder_path"] = path.join(
            settings["output_folder_path"], settings["static_folder_path"]
        )

        settings["favicon_ico"] = path.join(
            settings["main_folder_path"], settings["favicon_ico"]
        )
        settings["favicon_png"] = path.join(
            settings["main_folder_path"], settings["favicon_png"]
        )
        settings["favicon_svg"] = path.join(
            settings["main_folder_path"], settings["favicon_svg"]
        )
        settings["preview_png"] = path.join(
            settings["main_folder_path"], settings["preview_png"]
        )
        return settings
