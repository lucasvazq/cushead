import os
import typing


class Images:
    """Module to handle image tags"""

    def __init__(self, config, icons_config):
        self.config = config
        self.icons_config = icons_config

    def generate_head_images(self):
        favicons = []
        og_social_media_images = []
        twitter_social_media_images = []
        late_browser_config = []
        for image_type in self.icons_config.values():
            for brand in image_type:
                for config in brand.formated:
                    head_element = self._head_formater(
                        brand, config.file_name, config.size)
                    if head_element:
                        if brand.attribute_property.startswith('og:'):
                            og_social_media_images.append(head_element)
                        elif brand.attribute_name.startswith('twitter:'):
                            twitter_social_media_images.append(head_element)
                        elif brand.attribute_rel == "mask-icon" or brand.attribute_name == "msapplication-TileImage":
                            late_browser_config.append(head_element)
                        else:
                            favicons.append(head_element)
        return favicons, og_social_media_images, twitter_social_media_images, late_browser_config

    def _head_formater(
            self,
            brand_config,
            filenam,
            size: typing.Union[typing.List[int], None] = None,
    ):

        if not brand_config.head_output:
            return None

        size = size or [0, 0]
        tag_element_list = []
        new_file_path = os.path.join(brand_config.url_path, filenam)

        # order matter for legibility
        # tag
        # rel
        # name
        # property
        # special_content
        # special_href
        # content
        # type
        # sizes
        # color
        # title
        # media

        # tag name, example:
        # link
        if brand_config.tag_name:
            tag_element_list.append(f"{brand_config.tag_name}")

        # property, example:
        # ???
        if brand_config.attribute_property:
            tag_element_list.append(f"property='{brand_config.attribute_property}'")

        # name, example:
        # name="msapplication-TileImage"
        if brand_config.attribute_name:
            tag_element_list.append(f"name='{brand_config.attribute_name}'")

        # rel, example:
        # rel="icon"
        if brand_config.attribute_rel:
            tag_element_list.append(f"rel='{brand_config.attribute_rel}'")

        # type, example:
        # type="image/png"
        if brand_config.attribute_type:
            tag_element_list.append(f"type='{brand_config.attribute_type}'")

        # color, example:
        # ???
        if brand_config.attribute_color:
            tag_element_list.append(f"color='{brand_config.attribute_color}'")

        # Special sizes, example:
        # sizes="16x16"
        if brand_config.attribute_special_sizes:
            tag_element_list.append(f"sizes='{size[0]}x{size[1]}'")

        # content, example:
        # ???
        if brand_config.attribute_content:
            tag_element_list.append(f"content='{brand_config.attribute_content}'")

        # Special content and href. Example:
        # content="/static/ms-icon-144x144.png"
        # href="/static/favicon-16x16.png"
        # Both uses file_name and static url path
        if brand_config.attribute_special_content:
            tag_element_list.append(f"content='{new_file_path}'")
        if brand_config.attribute_special_href:
            tag_element_list.append(f"href='{new_file_path}'")

        # Special title, example:
        # title="Microsoft"
        if brand_config.attribute_special_title and self.config.get('title'):
            tag_element_list.append(f"title='{self.config['title']}'")

        # IN REVISION
        # media, example:
        # media="(device-min-width: 38px) and (device-min-height: 38px)"
        # Uses sizes_max_min
        if brand_config.sizes_max_min:
            tag_element_list.append(f"media='(device-width: {min(size[0], size[1]) // size[2]}px) and (device-height: {max(size[0], size[1]) // size[2]}px) and (-webkit-device-pixel-ratio: {size[2]}) and (orientation: {'portrait' if size[0] < size[1] else 'landscape'})'")

        return "<" + " ".join(tag_element_list) + ">"
