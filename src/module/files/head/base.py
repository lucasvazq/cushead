#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to handle the creation of tags that are inside the head tag

Classes:
    Head
"""

from src.module.files.head.images import Images
from src.module.files.head.general import General


class Head(General, Images):
    """Class to handle the creation of tags that become inside the head tag

    Methods:
        full_head -> list
        general -> list
        basic -> list
        complementary_files -> list
        social_media -> list
    """
    config = {}

    def full_head(self) -> list:
        """Return a list of tags related to the config of a website

        It's get the tags from the functions of the class: general, basic,
        complementary_files, social_media, and from the Parent class:
        favicon_ico, favicon_png, favicon_svg and preview_png.

        All of the tags are order with their importance
        """
        # The order matters
        head = [
            self.general(),
            self.basic(),
            self.wazuncho(),
            self.complementary_files(),
            self.social_media(),
        ]
        return head
