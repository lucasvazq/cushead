from os import path

from src2.helpers import FilesValidator, KeysValidator
from src2.services import format_sizes


class Images:
    icons_config: dict
    config: dict

    def _requirements(self, key):
        if key not in self.config:
            return False
        KeysValidator(key, value=self.config[key]).key_is_not_void()
        file_path = path.join(self.config.get('main_path', ''),
                              self.config[key])
        FilesValidator(self.config[key], file_path).path_is_file()
        return True

    def favicon_png(self):
        head = []
        if not self._requirements('favicon_png'): return head
        for icon_brand_config in self.icons_config.get('favicon_png', []):
            sizes = format_sizes(icon_brand_config)
            for size in sizes:
                filename = (f"{icon_brand_config['filename']}-"
                            f"{size[0]}x{size[1]}.png")
                element = self._icons_head_creator(filename, icon_brand_config,
                                                   size)
                head.append(element)
        return head

    def favicon_ico(self):
        head = []
        if not self._requirements('favicon_ico'): return head
        head.append( "<link rel='shortcut icon' "
                    f"href='/favicon.ico' type='image/x-icon' />")
        return head

    def favicon_svg(self):
        head = []
        if not self._requirements('favicon_svg'): return head
        color = self.config.get('background_color', '')
        filename = self.config.get('favicon_svg', '')
        head.append(f"<link rel='mask-icon' href='{filename}' "
                    f"color='{color}' />")
        return head

    def preview_png(self):
        head = []
        if not self._requirements('preview_png'): return head
        # og:image (http), og:image:secure_url (https) and twitter:image
        static_url = self.config.get('static_url', '')
        image = f"{static_url}preview.png"
        head.extend(
            f"<meta property='og:image' content='{image}' />",
            f"<meta property='og:image:secure_url' content='{image}' />",
            f"<meta name='twitter:image' content='{image}' />",
        )
        return head

    def _icons_head_creator(self, filename, icon_brand_config, size):
        min_size = size[1]
        if 'media' in icon_brand_config:
            size[1] = size[0]
        name_ref = icon_brand_config.get('name_ref', '')
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
