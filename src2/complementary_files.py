#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Handle the generations of files"""

import json
import os
from os import path

from PIL import Image
from resizeimage import resizeimage

from .helpers import (error_message, FilesHelper, FilesValidator,
                      FoldersHelper, KeysValidator)


class Icons:
    """Class related to icons generation"""

    brand = {}
    config = {}
    names = []

    
    def _requirements(self, key):
        if key not in self.config:
            return False
        KeysValidator.key_is_not_void(self.config[key], key)
        filepath = path.join(self.config['main_path'], self.config[key])
        FilesValidator.path_is_not_directory(filepath, key)
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
