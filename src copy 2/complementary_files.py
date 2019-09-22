#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Handle the generations of files"""

import json
import os
from os import path

from PIL import Image
from resizeimage import resizeimage

from .helpers import Errors, FilesHelper, FoldersHelper


def values(config):
    """
    Function used for return values

    Variables:
        names (list)
        brand (obj)

    names = [identifier (str)]

    brand: {
            identifier: {
                name_ref (str) Required
                filename (str) Required
                square_sizes (int list)
                non_square_sizes (list of int list)
                max_min (list of int list)
                content (str)
                file_type (str)
                title (str)
                metatag (bool)
                no_head (bool)
                verbosity (bool)
            }
        }

    identifier: only for identify objects inside brand object
    filename: filename of new resized image, its include extension and sizes
    max_min: used for generate medias queries
    content: used to replace the filename and set the static url to blank
    metatag: used to define tagname, attribute and ref variables
        True: 'meta', 'name', 'content'
        False: 'link', 'rel', 'href'
    no_head: used to determine if icon needs to be added to the head
    verbosity: used to determine if icon filename need to specify its sizes
        True: generate sizes variable with the next format:
            'size="SIZExSIZE"'
        False: generate blank variable named sizes

    Result:
    A: <link rel="shortcut icon" type="image/png" sizes="16x16"
        href="/static/favicon-16x16.png" />
    B: <link href="apple-touch-startup-image-320x320.png"
       media="screen and (min-device-width: 320px) and ... ..." />
    C: <link rel="fluid-icon" href="/static/fluidicon-512x512.png"
       title="Microsoft" />

    Template:
    <{} {}='{}' {}{}{}='{}{}' {}{}/>.format(
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
    """

    static_url = config.get('static_url', '')
    background_color = config.get('background_color', '')
    yandex_content = (
        f"logo={static_url}yandex.png, "
        f"color={background_color}"
    )

    # Order of how icons are generated and added to the head if it's
    # required
    # The order matters
    names = ['icon-sizes', 'windows', 'apple-touch-icon-default',
             'apple-touch-icon-sizes', 'apple-touch-startup-image-default',
             'apple-touch-startup-image', 'fluid-icon', 'browserconfig',
             'manifest', 'opensearch', 'yandex']
    brand = {
        'icon-sizes': {
            'name_ref': 'icon',
            'filename': 'favicon',
            # https://www.favicon-generator.org/
            # https://stackoverflow.com/questions/4014823/does-a-favicon-have-to-be-32x32-or-16x16
            # https://www.emergeinteractive.com/insights/detail/the-essentials-of-favicons/
            'square_sizes': [16, 24, 32, 48, 57, 60, 64, 70, 72, 76, 96,
                             114, 120, 128, 144, 150, 152, 167, 180, 192,
                             195, 196, 228, 310],
            'type': 'image/png',
            'verbosity': True,
        },
        'windows': {
            'name_ref': 'msapplication-TileImage',
            'filename': 'ms-icon',
            'square_sizes': [144],
            'metatag': True,
        },
        'apple-touch-icon-default': {
            'name_ref': 'apple-touch-icon',
            'filename': 'apple-touch-icon',
            'square_sizes': [57],
        },
        'apple-touch-icon-sizes': {
            'name_ref': 'apple-touch-icon',
            'filename': 'apple-touch-icon',
            'square_sizes': [57, 60, 72, 76, 114, 120, 144, 152, 167, 180,
                             1024],
            'verbosity': True,
        },
        'apple-touch-startup-image-default': {
            'name_ref': 'apple-touch-startup-image',
            'filename': 'launch',
            'square_sizes': [768],
        },
        'apple-touch-startup-image': {
            'name_ref': 'apple-touch-startup-image',
            'filename': 'launch',
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
        'fluid-icon': {
            'name_ref': 'fluid-icon',
            'filename': 'fluidicon',
            'square_sizes': [512],
            'title': 'Microsoft',
        },
        'browserconfig': {
            'name_ref': 'browserconfig',
            'filename': 'ms-icon',
            'square_sizes': [30, 44, 70, 150, 310],
            'non_square_sizes': [[310, 150]],
            'no_head': True,
        },
        'manifest': {
            'name_ref': 'manifest',
            'filename': 'android-icon',
            'square_sizes': [36, 48, 72, 96, 144, 192, 256, 384, 512],
            'file_type': 'image/png',
            'no_head': True,
            'verbosity': True,
        },
        'opensearch': {
            'name_ref': 'opensearch',
            'filename': 'opensearch',
            'sqyare_sizes': [16],
            'no_head': True,
            'verbosity': True,
        },
        'yandex': {
            'name_ref': 'yandex-tableau-widget',
            'filename': 'yandex',
            'square_sizes': [120],
            'metatag': True,
            'content': yandex_content,
        },
    }
    return [names, brand]


class Icons:
    """Class related to icons generation"""

    brand = {}
    config = {}
    names = []

    def _icons_head_creator(self, filename, name, size):

        if 'no_head' in self.brand[name]:
            return False

        min_size = size[1]
        if 'media' in self.brand[name]:
            size[1] = size[0]

        name_ref = self.brand[name]['name_ref']
        static_url = self.config['static_url']
        file_type = (
            f"type='{self.brand[name]['file_type']}' "
            if 'file_type' in self.brand[name] else ''
        )
        sizes = (
            f"sizes='{size[0]}x{size[1]}' "
            if 'verbosity' in self.brand[name] else ''
        )
        tagname, attribute, ref = (
            ('meta', 'name', 'content')
            if 'metatag' in self.brand[name] else
            ('link', 'rel', 'href')
        )
        title = (
            f"title='{self.brand[name]['title']}' "
            if 'title' in self.brand[name] else ''
        )
        media = (
            f"media=(min-device-width: {min_size}px) and "
            f"(min-device-height: {min_size}px) "
            if 'media' in self.brand[name] else ''
        )
        if 'content' in self.brand[name]:
            static_url = ''
            filename = f"content='{self.brand[name]['content']}'"

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

    def _requirements(self, key):
        if key not in self.config:
            return False
        Errors.void_key(self.config[key], key)
        filepath = path.join(self.config['main_path'], self.config[key])
        Errors.is_file(filepath, key)
        return True

    def _sizes_handler(self, image, name):
        """Resize 'favicon_png' to determinated sizes"""
        head = []

        # Get sizes
        square_sizes = self.brand[name].get('square_sizes', [])
        square_sizes = [[size, size] for size in square_sizes]
        non_square_sizes = self.brand[name].get('non_square_sizes', [])
        max_min = self.brand[name].get('squares_sizes', [])
        max_min = [size[0] for size in max_min]
        sizes = square_sizes + non_square_sizes + max_min

        for size in sizes:
            filename = (f"{self.brand[name]['filename']}-"
                        f"{size[0]}x{size[1]}.png")
            filepath = path.join(self.config['static_url_path'], filename)
            self.resize(image, size, filepath)

            # Some icons need to be added to head
            element = self._icons_head_creator(filename, name, size)
            if element:
                head.append(element)

        return head

    def favicon_png(self):
        """Generate .png icons"""

        if not self._requirements('favicon_png'):
            return []

        head = []

        # Open favicon_png file
        filepath = path.join(self.config['main_path'],
                             self.config['favicon_png'])
        with open(filepath, 'r+b') as file, \
                Image.open(file) as image:
            for name in self.names:
                head.append(self._sizes_handler(image, name))

        return head

    def favicon_ico(self):
        """favicon.ico"""

        if not self._requirements('favicon_ico'):
            return []

        # Root destination
        source = path.join(self.config['main_path'],
                           self.config['favicon_ico'])
        destination = path.join(self.config['output_path'], "favicon.ico")
        FilesHelper.copy_file(source, destination)

        string = ("<link rel='shortcut icon' "
                  f"href='/favicon.ico' type='image/x-icon' />")
        return string

    def favicon_svg(self):
        """favicon.svg"""

        if not self._requirements('favicon_svg'):
            return []

        source = path.join(self.config['main_path'],
                           self.config['favicon_svg'])
        destination = path.join(self.config['static_url_path'], "favicon.svg")
        FilesHelper.copy_file(source, destination)

        color = self.config.get('background_color', '')
        string = (f"<link rel='mask-icon' href='{self.config['favicon_svg']}' "
                  f"color='{color}' />")
        return string

    def preview_png(self):
        """preview.png"""

        if not self._requirements('preview_png'):
            return []

        source = path.join(self.config['main_path'],
                           self.config['preview_png'])
        destination = path.join(self.config['static_url_path'], "preview.png")
        FilesHelper.copy_file(source, destination)

        # og:image (http), og:image:secure_url (https) and twitter:image
        image = f"{self.config['static_url']}preview.png"
        head = [
            f"<meta property='og:image' content='{image}' />",
            f"<meta property='og:image:secure_url' content='{image}' />",
            f"<meta name='twitter:image' content='{image}' />",
        ]
        return head

    @staticmethod
    def resize(image, size, filepath):
        """Resize a image"""
        cover = resizeimage.resize_contain(image, [size[0], size[1]])
        cover.save(filepath, image.format)


class Others:
    """Class related to the generation of files that are not icons"""
    brand = {}
    config = {}

    def browserconfig(self):
        """browserconfig.xml"""
        string = ("<?xml version='1.0' encoding='utf-8'?><browserconfig>"
                  "<msapplication><tile>")
        string += ''.join([
            "<square{0}x{0}logo src='{1}{2}-{0}x{0}.png' />".format(
                size,
                self.config['static_url'],
                self.brand['browserconfig']['filename']
            )
            for size in self.brand['browserconfig']['square_sizes']
        ])
        string += ''.join([
            "<wide{0}x{1}logo src='{2}{3}-{0}x{1}.png' />".format(
                size[0],
                size[1],
                self.config['static_url'],
                self.brand['browserconfig']['filename']
            )
            for size in self.brand['browserconfig']['non_square_sizes']
        ])
        color = self.config.get('background_color', '')
        string += (f"<TileColor>{color}</TileColor></tile></msapplication>"
                   "</browserconfig>")
        string = string.replace('\'', '"')
        head = ("<meta name='msapplication-config' "
                f"content='{self.config['static_url']}browserconfig.xml' />")
        return [string, head]

    def manifest(self):
        """manifest.json"""
        urlpath = self.config['static_url']
        icons = [
            {
                'src': "{0}{1}-{2}x{2}".format(
                    urlpath, self.brand['manifest']['filename'], size
                ),
                'sizes': f"{size}x{size}",
                'type': 'image/png',
                'density': str(size / 48)
            }
            for size in self.brand['manifest']['square_sizes']
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
        if 'background_color' in self.config:
            dictionary['background_color'] = self.config['background_color']
            dictionary['theme_color'] = self.config['background_color']
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
        """opensearch.xml"""
        title = self.config.get('title', '')
        url = self.config.get('url', '')
        static_url = self.config['static_url']
        string = ("<?xml version='1.0' encoding='utf-8'?>"
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
        string = string.replace('\'', '"')
        head = ("<link rel='search' "
                f"type='application/opensearchdescription+xml' "
                f"title='{title}' href='{static_url}opensearch.xml' />")
        return [string, head]

    def robots(self):
        """robots.txt"""
        protocol = self.config.get('protocol', '')
        sitemap_content = (
            "\n"
            f"Sitemap: {protocol}{self.config['clean_url']}/sitemap.xml"
            if 'sitemap' in self.config else ''
        )
        string = ("User-agent: *\n"
                  "Allow: /\n"
                  f"{sitemap_content}")
        return string

    def sitemap(self):
        """sitemap.xml"""
        protocol = self.config.get('protocol', '')
        string = ("<?xml version='1.0' encoding='uft-8'?>"
                  "<urlset xmlns="
                  "'http://www.sitemaps.org/schemas/sitemap/0.9' "
                  "xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' "
                  "xsi:schemaLocation="
                  "'http://www.sitemaps.org/schemas/sitemap/0.9 "
                  "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'>"
                  f"<url><loc>{protocol}{self.config['clean_url']}/</loc>"
                  "</url></urlset>")
        string = string.replace('\'', '"')
        return string


class ComplementaryFiles(Icons, Others):
    """Main class of this module"""
    config = {}

    def __init__(self):

        self.names, self.brand = values(self.config)

    def generate(self):
        """Generate HTML head elements and new files"""

        head = []

        # Favicon .png version
        # Multiples elements
        elements = self.favicon_png()
        head.extend(elements)

        # Favicon .ico version
        # Only one element
        element = self.favicon_ico()
        head.append(element)

        # Favicon .svg version
        # Only one element
        element = self.favicon_svg()
        head.append(element)

        # Preview .png
        # Multiples elements
        elements = self.preview_png()
        head.extend(elements)

        # browserconfig.xml
        browserconfig_content, browserconfig_head = self.browserconfig()
        head.append(browserconfig_head)
        filepath = path.join(self.config['static_url_path'],
                             'browserconfig.xml')
        FilesHelper.write_file(filepath, browserconfig_content)

        # manifest.json
        manifest_content, manifest_head = self.manifest()
        head.append(manifest_head)
        filepath = path.join(self.config['static_url_path'], 'manifest.json')
        FilesHelper.write_file(filepath, manifest_content)

        # opensearch.xml
        opensearch_content, opensearch_head = self.opensearch()
        head.append(opensearch_head)
        filepath = path.join(self.config['static_url_path'], 'opensearch.xml')
        FilesHelper.write_file(filepath, opensearch_content)

        if 'clean_url' in self.config:
            # robots.txt
            robots_content = self.robots()
            filepath = path.join(self.config['output_path'], 'robots.txt')
            FilesHelper.write_file(filepath, robots_content)

            # sitemap.xml
            sitemap_content = self.sitemap()
            filepath = path.join(self.config['output_path'], 'sitemap.xml')
            FilesHelper.write_file(filepath, sitemap_content)

        return head
