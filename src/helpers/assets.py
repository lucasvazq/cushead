#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module to handle the assets

Classes:
    Images
"""

from typing import List


class Images:
    """Handle the images of the assets

    Methods:
        @staticmethod images_list -> List[str]
    """

    @staticmethod
    def images_list() -> List[str]:
        """Returns a list of image file names that are in assets"""
        return [
            'favicon_ico_16px.ico',
            'favicon_png_1600px.png',
            'favicon_svg_scalable.svg',
            'preview_png_500px.png',
        ]
