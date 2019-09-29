#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from typing import List

from src.helpers.validators import FilesValidator, KeysValidator
from src.services.images import ImageService


class Images(ImageService):
    icons_config: {}
    config: {}

    def _requirements(self, key):
        if key not in self.config:
            return False
        KeysValidator(key=key, value=self.config.get(key, '')).key_is_not_void()
        file_path = path.join(self.config.get('main_folder_path', ''),
                              self.config[key])
        FilesValidator(file_path=file_path, key=self.config[key]).path_is_not_directory()
        return True

    def favicon_png(self):
        head = []
        if not self._requirements('favicon_png'):
            return head
        for icon_brand_config in self.icons_config.get('favicon_png', []):
            sizes = self.format_sizes(icon_brand_config)
            for size in sizes:
                head.append(self._icons_head_creator(icon_brand_config, size))
        return head

    def favicon_ico(self):
        head = []
        if not self._requirements('favicon_ico'):
            return head
        head.append(f"<link rel='shortcut icon' "
                    f"href='/favicon.ico' type='image/x-icon' />")
        return head

    def favicon_svg(self):
        head = []
        if not self._requirements('favicon_svg'):
            return head
        color = self.config.get('background_color', '')
        head.append(f"<link rel='mask-icon' href='favicon.svg' "
                    f"color='{color}' />")
        return head

    def preview_png(self):
        head = []
        if not self._requirements('preview_png'):
            return head
        # og:image (http), og:image:secure_url (https) and twitter:image
        image = f"{self.config.get('static_url', '')}/preview.png"
        head.extend([
            f"<meta property='og:image' content='{image}' />",
            f"<meta property='og:image:secure_url' content='{image}' />",
            f"<meta name='twitter:image' content='{image}' />",
        ])
        return head

    def _icons_head_creator(self, icon_brand_config, size: List[int] = [0, 0]):
        # tag name
        tag_name = (
            f"{icon_brand_config.tag_name} "
            if getattr(icon_brand_config, 'tag_name', '') else ''
        )
        # content=""
        attribute_content = (
            (
                f"content='{icon_brand_config.attribute_content}' "
                    .replace('\'', '"')
            )
            if getattr(icon_brand_config, 'attribute_content', '') else ''
        )
        # name=""
        attribute_name = (
            (
                f"name='{icon_brand_config.attribute_name}' "
                    .replace('\'', '"')
            )
            if getattr(icon_brand_config, 'attribute_name', '') else ''
        )
        # rel=""
        attribute_rel = (
            (
                f"rel='{icon_brand_config.attribute_rel}' "
                    .replace('\'', '"')
            )
            if getattr(icon_brand_config, 'attribute_rel', '') else ''
        )
        # title=""
        attribute_title = (
            (
                f"title='{icon_brand_config.attribute_title}' "
                    .replace('\'', '"')
            )
            if getattr(icon_brand_config, 'attribute_tittle', '') else ''
        )
        # type=""
        attribute_type = (
            (
                f"type='{icon_brand_config.attribute_type}' "
                    .replace('\'', '"')
            )
            if getattr(icon_brand_config, 'attribute_type', '') else ''
        )
        # href=""
        file_name = getattr(icon_brand_config, 'file_name', '')
        new_file_name = f"{file_name}-{size[0]}x{size[1]}.png"
        attribute_special_href = (
            (
                "href='{}' ".format(
                    path.join(
                        self.config.get('static_url', ''),
                        new_file_name,
                    )
                ).replace('\'', '"')
            )
            if getattr(icon_brand_config, 'attribute_special_href', False)
            else ''
        )
        # sizes=""
        attribute_special_sizes = (
            (
                f"sizes='{size[0]}x{size[1]}' "
                    .replace('\'', '"')
            )
            if getattr(icon_brand_config, 'attribute_special_sizes', False)
            else ''
        )

        element = (
            f"<{tag_name}"
            f"{attribute_content}"
            f"{attribute_name}"
            f"{attribute_rel}"
            f"{attribute_title}"
            f"{attribute_type}"
            f"{attribute_special_href}"
            f"{attribute_special_sizes}"
            f"/>"
        )
        return element
