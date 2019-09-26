#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to handle the images configurations

Classes DefaultIconsFormatConfig
"""

from os import path

from src.services.images import ImageService


class DefaultIconsFormatConfig:
    config: dict

    def _png_icons_config(self):
        yandex_content = (f"logo={self.config.get('static_url', '')}"
                          "/yandex.png, "
                          f"color={self.config.get('background_color', '')}")
        return [
            # default png favicons
            {
                'name_ref': 'icon',
                'file_name': 'favicon',
                # https://www.favicon-generator.org/
                # https://stackoverflow.com/questions/4014823/does-a-favicon-have-to-be-32x32-or-16x16
                # https://www.emergeinteractive.com/insights/detail/the-essentials-of-favicons/
                'square_sizes': [16, 24, 32, 48, 57, 60, 64, 70, 72, 76, 96,
                                 114, 120, 128, 144, 150, 152, 167, 180, 192,
                                 195, 196, 228, 310],
                'type': 'image/png',
                'verbosity': True,
            },
            # windows favicon
            {
                'name_ref': 'msapplication-TileImage',
                'file_name': 'ms-icon',
                'square_sizes': [144],
                'metatag': True,
            },
            # apple touch default
            {
                'name_ref': 'apple-touch-icon',
                'file_name': 'apple-touch-icon',
                'square_sizes': [57],
            },
            # apple touch with differents sizes
            {
                'name_ref': 'apple-touch-icon',
                'file_name': 'apple-touch-icon',
                'square_sizes': [57, 60, 72, 76, 114, 120, 144, 152, 167, 180,
                                 1024],
                'verbosity': True,
            },
            # apple touch startup image default
            {
                'name_ref': 'apple-touch-startup-image',
                'file_name': 'launch',
                'square_sizes': [768],
            },
            # apple touch startup image with differents sizes
            {
                'name_ref': 'apple-touch-startup-image',
                'file_name': 'launch',
                # Based on:
                # https://css-tricks.com/snippets/css/media-queries-for-standard-devices/
                'max_min': [
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
            },
            # Mac fluid icon
            {
                'name_ref': 'fluid-icon',
                'file_name': 'fluidicon',
                'square_sizes': [512],
                'title': self.config.get('title', ''),
            },
            # yandex browser
            {
                'name_ref': 'yandex-tableau-widget',
                'file_name': 'yandex',
                'square_sizes': [120],
                'metatag': True,
                'content': yandex_content,
            },
        ]

    @staticmethod
    def _browserconfig_icons_config():
        return {
            'name_ref': 'browserconfig',
            'file_name': 'ms-icon',
            'square_sizes': [30, 44, 70, 150, 310],
            'non_square_sizes': [[310, 150]],
        }

    @staticmethod
    def _manifest_icons_config():
        return {
            'name_ref': 'manifest',
            'filename': 'android-icon',
            'square_sizes': [36, 48, 72, 96, 144, 192, 256, 384, 512],
            'file_type': 'image/png',
            'verbosity': True,
        }

    @staticmethod
    def _opensearch_icons_config():
        return {
            'name_ref': 'opensearch',
            'filename': 'opensearch',
            'sqyare_sizes': [16],
            'verbosity': True,
        }

    def default_icons_config(self):
        return {
            'favicon_png': self._png_icons_config(),
            'browserconfig': self._browserconfig_icons_config(),
            'manifest': self._manifest_icons_config(),
            'opensearch': self._opensearch_icons_config(),
        }


class DefaultImagesCreationConfig(ImageService):
    config: dict
    icons_config: dict

    def _favicon_ico(self):
        favicon_ico = self.config.get('favicon_ico', '')
        if not favicon_ico:
            return []
        return [{
            'destination_file_path': path.join(
                self.config.get('output_folder_path'),
                'favicon.ico'
            ),
            'source_file_path': path.join(
                self.config.get('main_folder_path', ''),
                favicon_ico
            ),
        }]

    def _favicon_png(self):
        images_format = []
        favicon_png = self.config.get('favicon_png', '')
        if not favicon_png:
            return images_format
        source_file_path = path.join(self.config.get('main_folder_path', ''),
                                     favicon_png)
        for brand_icon_config in self.icons_config.get('favicon_png', []):
            file_name = brand_icon_config.get('file_name', '')
            for size in self.format_sizes(brand_icon_config):
                destination_file_path = path.join(
                    self.config.get('static_folder_path', ''),
                    f"{file_name}-{size[0]}x{size[1]}.png")
                images_format.append({
                    'destination_file_path': destination_file_path,
                    'resize': True,
                    'size': size,
                    'source_file_path': source_file_path,
                })
        return images_format

    def _favicon_svg(self):
        favicon_svg = self.config.get('favicon_svg', '')
        if not favicon_svg:
            return []
        return [{
            'destination_file_path': path.join(
                self.config.get('static_folder_path'),
                'favicon.svg'
            ),
            'source_file_path': path.join(
                self.config.get('main_folder_path', ''),
                favicon_svg
            ),
        }]

    def _preview_png(self):
        preview_png = self.config.get('preview_png', '')
        if not preview_png:
            return []
        return [{
            'destination_file_path': path.join(
                self.config.get('static_folder_path'),
                'preview-500x500.png'
            ),
            'resize': True,
            'size': [500, 500],
            'source_file_path': path.join(
                self.config.get('main_folder_path', ''),
                preview_png
            )
        }]

    def default_images_creation_config(self):
        images_creation_config = [
            self._favicon_ico(),
            self._favicon_png(),
            self._favicon_svg(),
            self._preview_png(),
        ]
        return [
            element for group in images_creation_config
            for element in group
        ]
