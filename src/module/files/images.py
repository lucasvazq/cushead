#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from typing import List

from src.helpers.validators import FilesValidator, KeysValidator
from src.services.images import ImageService


class Images(ImageService):
    icons_config: {}
    config: {}

    def _icons_head_creator(self, icon_brand_config, size: List[int] = [0, 0]):

        tag_element_list = ['<']

        # tag name, example:
        # link
        tag_element_list.append(
            f"{icon_brand_config.tag_name} "
            if getattr(icon_brand_config, 'tag_name', '') else ''
        )

        # content, example:
        # ???
        tag_element_list.append(
            f"content='{icon_brand_config.attribute_content}' "
            if getattr(icon_brand_config, 'attribute_content', '') else ''
        )

        # name, example:
        # name="msapplication-TileImage"
        tag_element_list.append(
            f"name='{icon_brand_config.attribute_name}' "
            if getattr(icon_brand_config, 'attribute_name', '') else ''
        )
        
        # rel, example:
        # rel="icon"
        tag_element_list.append(
            f"rel='{icon_brand_config.attribute_rel}' "
            if getattr(icon_brand_config, 'attribute_rel', '') else ''
        )

        # type, example:
        # type="image/png"
        tag_element_list.append(
            f"type='{icon_brand_config.attribute_type}' "
            if getattr(icon_brand_config, 'attribute_type', '') else ''
        )

        # Special content and href. Example:
        # content="/static/ms-icon-144x144.png"
        # href="/static/favicon-16x16.png"
        # Both uses file_name and static url path
        file_name = getattr(icon_brand_config, 'file_name', '')
        new_file_name = f"{file_name}-{size[0]}x{size[1]}.png"
        new_file_path = path.join(self.config.get('static_url', ''),
                                  new_file_name)
        tag_element_list.append(
            f"content='{new_file_path}' "
            if getattr(icon_brand_config, 'attribute_special_content', False)
            else ''
        )
        tag_element_list.append(
            f"href='{new_file_path}' "
            if getattr(icon_brand_config, 'attribute_special_href', False)
            else ''
        )

        # Special title, example:
        # title="Microsoft"
        title = self.config.get('title', '')
        tag_element_list.append(
            f"title='{title}' "
            if getattr(icon_brand_config, 'attribute_special_title', False)
            else ''
        )

        # Special sizes, example:
        # sizes="16x16"
        tag_element_list.append(
            f"sizes='{size[0]}x{size[1]}' "
            if getattr(icon_brand_config, 'attribute_special_sizes', False)
            else ''
        )

        # media, example:
        # media="(device-min-width: 38px) and (device-min-height: 38px)"
        # Uses sizes_max_min
        min_size = ''
        for max_min in getattr(icon_brand_config, 'sizes_max_min', []):
            if size[0] == max_min[1]:
                min_size = max_min[0]
        tag_element_list.append(
            (
                f"media='(device-min-width: {min_size}px) and "
                f"(device-min-height: {min_size}px)' "
            )
            if getattr(icon_brand_config, 'sizes_max_min', []) else ''
        )

        tag_element_string = ''.join(tag_element_list)
        tag_element_string = tag_element_string[:-1]
        tag_element_string += ' />'
        return tag_element_string

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
        static_url = self.config.get('static_url', '')
        head.append(f"<link rel='mask-icon' href='{static_url}/favicon.svg' "
                    f"color='{color}' />")
        return head

    def preview_png(self):
        head = []
        if not self._requirements('preview_png'):
            return head
        # og:image (http), og:image:secure_url (https) and twitter:image
        image = f"{self.config.get('static_url', '')}/preview-500x500.png"
        head.extend([
            f"<meta property='og:image' content='{image}' />",
            f"<meta property='og:image:secure_url' content='{image}' />",
            f"<meta name='twitter:image' content='{image}' />",
        ])
        return head
