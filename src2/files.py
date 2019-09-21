from os import path



class Icons:
    icons_config = {
        'head_index': []
    }
    config = {}

    def icons(self):
        head = []
        for icon_brand_config in self.icons_config['head_index']:
            # Get sizes
            square_sizes = icon_brand_config.get('square_sizes', [])
            square_sizes = [[size, size] for size in square_sizes]
            non_square_sizes = icon_brand_config.get('non_square_sizes', [])
            max_min = icon_brand_config.get('squares_sizes', [])
            max_min = [size[0] for size in max_min]
            sizes = square_sizes + non_square_sizes + max_min

            for size in sizes:
                filename = (f"{icon_brand_config['filename']}-"
                            f"{size[0]}x{size[1]}.png")
                element = self._icons_head_creator(filename, icon_brand_config,
                                                   size)
                head.append(element)

        return head

    def _icons_head_creator(self, filename, icon_brand_config, size):
        min_size = size[1]
        if 'media' in icon_brand_config:
            size[1] = size[0]

        name_ref = icon_brand_config['name_ref']
        static_url = self.config['static_url']
        file_type = (
            f"type='{icon_brand_config['file_type']}' "
            if 'file_type' in icon_brand_config else ''
        )
        sizes = (
            f"sizes='{size[0]}x{size[1]}' "
            if 'verbosity' in icon_brand_config else ''
        )
        tagname, attribute, ref = (
            ('meta', 'name', 'content')
            if 'metatag' in icon_brand_config else
            ('link', 'rel', 'href')
        )
        title = (
            f"title='{icon_brand_config['title']}' "
            if 'title' in icon_brand_config else ''
        )
        media = (
            f"media=(min-device-width: {min_size}px) and "
            f"(min-device-height: {min_size}px) "
            if 'media' in icon_brand_config else ''
        )
        if 'content' in icon_brand_config:
            static_url = ''
            filename = f"content='{icon_brand_config['content']}'"

        # Keep using format function for better reference to each element of
        # the formated string
        # A: <link rel="shortcut icon" type="image/png" sizes="16x16"
        #    href="/static/favicon-16x16.png" />
        # B: <link href="apple-touch-startup-image-320x320.png"
        #    media="screen and (min-device-width: 320px) and ... ..." />
        # C: <link rel="fluid-icon" href="/static/fluidicon-512x512.png"
        #    title="Microsoft" />
        element = "<{} {}='{}' {}{}{}='{}{}' {}{}/>".format(
            tagname,  # A: link
            attribute,  # A: rel
            name_ref,  # A: shortcut icon
            file_type,  # A: type="image/png"
            sizes,  # A: sizes="16x16"
            ref,  # A: href
            static_url,  # A: /static/
            filename,  # A: favicon-16x16.png
            media,  # B: media="screen and (min-device-width: 320px) and ...
            title,  # C: title="Microsoft"
        )
        return element

class Head(Icons):
    def full_head(self):
        icons = self.icons()
        head = self.head
        return icons + head

    def head(self):
        pass

class Index(Head):
    
    def full(self):
        head = self.full_head
        html = self.html(head)
        return html
    
    def html(self, head):
        return ''

class Browserconfig:
    # return string
    pass

class Files(Index, Browserconfig):
    pass