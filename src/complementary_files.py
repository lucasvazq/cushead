#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import textwrap
from os import path

from PIL import Image
from resizeimage import resizeimage

from .helpers import Helpers


class Values:

    def __init__(self):
        self.names = ['icon-sizes', 'windows', 'apple-touch-icon-default',
                      'apple-touch-icon-sizes', 'apple-touch-startup-image',
                      'fluid-icon', 'browserconfig', 'manifest', 'opensearch']
        self.brand = {
            'icon-sizes': {
                'name_ref': 'icon',
                'name': 'favicon',
                # https://www.favicon-generator.org/
                # https://stackoverflow.com/questions/4014823/does-a-favicon-have-to-be-32x32-or-16x16
                # https://www.emergeinteractive.com/insights/detail/the-essentials-of-favicons/
                'sizes': [16, 24, 32, 48, 57, 60, 64, 70, 72, 76, 96, 114, 120,
                          128, 144, 150, 152, 167, 180, 192, 195, 196, 228,
                          310],
                'verbosity': True,
                'type': 'image/png',
            },
            'windows': {
                'name_ref': 'msapplication-TileImage',
                'name': 'ms-icon',
                'sizes': [144],
                'metatag': True,
            },
            'apple-touch-icon-default': {
                'name_ref': 'apple-touch-icon',
                'name': 'apple-touch-icon',
                'sizes': [57],
            },
            'apple-touch-icon-sizes': {
                'name_ref': 'apple-touch-icon',
                'name': 'apple-touch-icon',
                'sizes': [57, 60, 72, 76, 114, 120, 144, 152, 167, 180, 1024],
                'verbosity': True,
            },
            'apple-touch-startup-image': {
                'name_ref': 'apple-touch-startup-image',
                'name': 'launch',
                'sizes': [768],
            },
            'fluid-icon': {
                'name_ref': 'fluid-icon',
                'name': 'fluidicon',
                'sizes': [512],
                'title': 'Microsoft',
            },
            'browserconfig': {
                'name_ref': 'browserconfig',
                'name': 'ms-icon',
                'sizes': [30, 44, 70, 150, 310],
                'special_sizes': [[310, 150]],
                'no-head': True,
            },
            'manifest': {
                'name_ref': 'manifest',
                'name': 'android-icon',
                'sizes': [36, 48, 72, 96, 144, 192, 256, 384, 512],
                'verbosity': True,
                'type': 'image/png',
                'no-head': True,
            },
            'opensearch': {
                'name_ref': 'opensearch',
                'name': 'opensearch',
                'sizes': [16],
                'verbosity': True,
                'no-head': True,
            },
        }
        super().__init__()


class Icons:
    brand = None
    config = None

    def __init__(self):
        super().__init__()

    def general_icons(self, filename, name, size):
        if 'no-head' in self.brand[name]:
            return None
        verbosity = (
            f"sizes='{size[0]}x{size[1]}' "
            if 'verbosity' in self.brand[name] else ''
        )
        tagname, attribute, ref = (
            ('meta', 'name', 'content')
            if 'metatag' in self.brand[name] else
            ('link', 'rel', 'href')
        )
        file_type = (
            f"type='{self.brand[name]['type']}' "
            if 'type' in self.brand[name] else ''
        )
        title = (
            f"title='{self.brand[name]['title']}' "
            if 'title' in self.brand[name] else ''
        )
        # Keep using format function for better reference to each element of the
        # formated string
        # A: <link rel="shortcut icon" type="image/png" sizes="16x16"
        #    href="/static/favicon-16x16.png" />
        # B: <link rel="fluid-icon" href="/static/fluidicon-512x512.png"
        #    title="Microsoft" />
        name_ref = self.brand[name]['name_ref']
        static_url = self.config['static_url']
        element = "<{} {}='{}' {}{}{}='{}{}' {}/>".format(
            tagname,  # A: link
            attribute,  # A: rel
            name_ref,  # A: shortcut icon
            file_type,  # A: type="image/png"
            verbosity,  # A: sizes="16x16"
            ref,  # A: href
            static_url,  # A: /static/
            filename,  # A: favicon-16x16.png
            title,  # B: title="Microsoft"
        )
        return element

    def favicon_ico(self):
        if 'favicon_ico' in self.config:
            s = ("<link rel='shortcut icon' "
                 f"href='/{self.config['favicon_ico']}' type='image/x-icon' />")
            return s

    def favicon_svg(self):
        if 'favicon_svg' in self.config:
            color = self.config.get('color', '')
            s = (f"<link rel='mask-icon' href='{self.config['favicon_svg']}' "
                 f"color='{color}' />")
            return s

    @staticmethod
    def resize(image, size, filepath):
        print(size)
        cover = resizeimage.resize_contain(image, [size[0], size[1]])
        cover.save(filepath, image.format)


class Others:
    brand = None
    config = None

    def __init__(self):
        super().__init__()

    def browserconfig(self):
        s = ("<?xml version='1.0' encoding='utf-8'?><browserconfig>"
             "<msapplication><tile>")
        s += ''.join([
            "<square{0}x{0}logo src='{1}{2}-{0}x{0}.png' />".format(
                size,
                self.config['static_url'],
                self.brand['browserconfig']['name']
            )
            for size in self.brand['browserconfig']['sizes']
        ])
        s += ''.join([
            "<wide{0}x{1}logo src='{2}{3}-{0}x{1}.png' />".format(
                size[0],
                size[1],
                self.config['static_url'],
                self.brand['browserconfig']['name']
            )
            for size in self.brand['browserconfig']['special_sizes']
        ])
        color = self.config.get('color', '')
        s += (f"<TileColor>{color}</TileColor></tile></msapplication>"
              "</browserconfig>")
        s = s.replace('\'', '"')
        head = ("<meta name='msapplication-config' "
                f"content='{self.config['static_url']}browserconfig.xml' />")
        return [s, head]

    def manifest(self):
        urlpath = self.config['static_url']
        icons = [
            {
                'src': "{0}{1}-{2}x{2}".format(
                    urlpath, self.brand['manifest']['name'], size
                ),
                'sizes': f"{size}x{size}",
                'type': 'image/png',
                'density': str(size / 48)
            }
            for size in self.brand['manifest']['sizes']
        ]
        dictionary = {}
        if 'title' in self.config:
            dictionary['name'] = self.config['title']
            dictionary['short_name'] = self.config['title']
        if 'description' in self.config:
            dictionary['description'] = self.config['description']
        if 'dir' in self.config:
            dictionary['dir'] = self.config['dir']
        if 'start_url' in self.config:
            dictionary['start_url'] = self.config['start_url']
        if 'orientation' in self.config:
            dictionary['orientation'] = self.config['orientation']
        if 'color' in self.config:
            dictionary['background_color'] = self.config['color']
            dictionary['theme_color'] = self.config['color']
        if 'language' in self.config:
            dictionary['default_locale'] = self.config['language']
        if 'scope' in self.config:
            dictionary['scope'] = self.config['scope']
        if 'display' in self.config:
            dictionary['display'] = self.config['display']
        if 'platform' in self.config:
            dictionary['platform'] = self.config['platform']
        if 'applications' in self.config:
            dictionary['related_applications'] = self.config['applications']
        dictionary['icons'] = icons
        dictionary = json.dumps(dictionary)
        head = (f"<link rel='manifest' href='{self.config['static_url']}"
                f"manifest.json' />")
        return [dictionary, head]

    def opensearch(self):
        title = self.config.get('title', '')
        url = self.config.get('url', '')
        static_url = self.config['static_url']
        s = ("<?xml version='1.0' encoding='utf-8'?>"
             "<OpenSearchDescription xmlns:moz='"
             "http://www.mozilla.org/2006/browser/search/' "
             "xmlns='http://a9.com/-/spec/opensearch/1.1/'>"
             "</OpenSearchDescription>"
             f"<ShortName>{title}</ShortName>"
             f"<Description>Search {title}</Description>"
             "<InputEncoding>UTF-8</InputEncoding>"
             "<Url method='get' type='text/html' "
             "template='http://www.google.com/search?q="
             f"{{searchTerms}}+site%3A{url}' />"
             "<Image height='16' width='16' type='image/png'>"
             f"{static_url}opensearch-16x16.png"
             "</Image>")
        s = s.replace('\'', '"')
        head = ("<link rel='search' "
                f"type='application/opensearchdescription+xml' title='{title}' "
                f"href='{static_url}opensearch.xml' />")
        return [s, head]

    def robots(self):
        protocol = self.config.get('protocol', '')
        sitemap_content = (
            f"Sitemap: {protocol}{self.config['clear_url']}/sitemap.xml"
            if 'sitemap' in self.config else ''
        )
        s = ("User-agent: *\n"
             "Allow: /\n"
             "\n"
             f"{sitemap_content}")
        return s

    def sitemap(self):
        protocol = self.config.get('protocol', '')
        s = ("<?xml version='1.0' encoding='uft-8'?>"
             "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9' "
             "xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' "
             "xsi:schemaLocation='http://www.sitemaps.org/schemas/sitemap/0.9 "
             "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'>"
             f"<url><loc>{protocol}{self.config['clear_url']}/</loc></url>"
             "</urlset>")
        s = s.replace('\'', '"')
        return s


class ComplementaryFiles(Values, Icons, Others, Helpers):
    config = None

    def __init__(self):
        super().__init__()

    def generate(self):
        head, new_files = ([], [])

        # Create folder for statics folder
        static_folderpath = path.join(self.config['files_output'],
                                      self.config['static_url'])
        static_folderpath = path.join(os.getcwd(), static_folderpath)
        self.create_folder(static_folderpath)

        if 'favicon_png' in self.config:

            # Test: test_void_icon_png
            # Action: get in
            if not len(self.config['favicon_png']):
                self.error_message("'favicon_png' key value can't be void.")

            # Test: test_icon_png_doesnt_exists
            # Action: get in
            if not path.isfile(self.config['favicon_png']):
                filepath = path.join(os.getcwd(), self.config['favicon_png'])
                e = (
                    f"'favicon_png' key ({self.config['favicon_png']}) must be "
                    "referred to a file path that exists."
                    f"FILE PATH: {filepath}"
                )
                self.error_message(e)

            # General icons
            with open(self.config['favicon_png'], 'r+b') as f, \
                    Image.open(f) as image:
                for name in self.names:

                    # Resize 'favicon_png' to determinated sizes

                    # Square icons, e.g., 16x16
                    sizes = self.brand[name].get('sizes', [])
                    for size in sizes:
                        filename = (f"{self.brand[name]['name']}-"
                                    f"{size}x{size}.png")
                        filepath = path.join(static_folderpath, filename)
                        self.resize(image, [size, size], filepath)
                        new_files.append(filepath)
                        # Some square icons are added to head
                        # The function 'general_icons' can return a String for
                        # this cases
                        element = self.general_icons(filename, name,
                                                     [size, size])
                        if element:
                            head.append(element)

                    # Non square icons, e.g., 310x150
                    sizes = self.brand[name].get('special_sizes', [])
                    for size in sizes:
                        filename = (f"{self.brand[name]['name']}-"
                                    f"{size[0]}x{size[1]}.png")
                        filepath = path.join(static_folderpath, filename)
                        self.resize(image, size, filepath)
                        new_files.append(filepath)
                        # Non square icons aren't added to head
                        # The function 'general_icons' returns always None for
                        # this cases
                        self.general_icons(filename, name, size)

            # Favicon .ico version
            element = self.favicon_ico()
            if element:
                head.append(element)

            # Favicon .svg version
            element = self.favicon_svg()
            if element:
                head.append(element)

            # browserconfig.xml
            browserconfig_content, browserconfig_head = self.browserconfig()
            head.append(browserconfig_head)
            filepath = path.join(static_folderpath, 'browserconfig.xml')
            self.write_file(filepath, browserconfig_content)
            new_files.append(filepath)

            # manifest.json
            manifest_content, manifest_head = self.manifest()
            head.append(manifest_head)
            filepath = path.join(static_folderpath, 'manifest.json')
            self.write_file(filepath, manifest_content)
            new_files.append(filepath)

            # opensearch.xml
            opensearch_content, opensearch_head = self.opensearch()
            head.append(opensearch_head)
            filepath = path.join(static_folderpath, 'opensearch.xml')
            self.write_file(filepath, opensearch_content)
            new_files.append(filepath)

            if 'clear_url' in self.config:

                # robots.txt
                robots_content = self.robots()
                filepath = path.join(self.config['files_output'], 'robots.txt')
                self.write_file(filepath, robots_content)
                new_files.append(filepath)

                # sitemap.xml
                sitemap_content = self.sitemap()
                filepath = path.join(self.config['files_output'], 'sitemap.xml')
                self.write_file(filepath, sitemap_content)
                new_files.append(filepath)

        return head, new_files
