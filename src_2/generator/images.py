class Images:
    """Module to handle image tags"""

    def __init__(self, config):
        self.config = config

    def icons_head_creator(self, icon_brand_config, filenam,
                            size: Union[List[int], None] = None):

        if not getattr(icon_brand_config, 'head_output', False):
            return None

        size = size or [0, 0]

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

        tag_element_list = list('<')

        # tag name, example:
        # link
        tag_element_list.append(
            f"{icon_brand_config.tag_name} "
            if getattr(icon_brand_config, 'tag_name', '') else ''
        )

        # color, example:
        # ???
        tag_element_list.append(
            f"color='{icon_brand_config.attribute_color}' "
            if getattr(icon_brand_config, 'attribute_color', '') else ''
        )

        # content, example:
        # ???
        tag_element_list.append(
            f"content='{icon_brand_config.attribute_content}' "
            if getattr(icon_brand_config, 'attribute_content', '') else ''
        )

        # property, example:
        # ???
        tag_element_list.append(
            f"property='{icon_brand_config.attribute_property}' "
            if getattr(icon_brand_config, 'attribute_property', '') else ''
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
        url_path = getattr(icon_brand_config, 'url_path', '')
        new_file_path = path.join(url_path, filenam)
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

        # Special sizes, example:
        # sizes="16x16"
        tag_element_list.append(
            f"sizes='{size[0]}x{size[1]}' "
            if getattr(icon_brand_config, 'attribute_special_sizes', False)
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

        # IN REVISION
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
        tag_element_string += '>'

        return tag_element_string
