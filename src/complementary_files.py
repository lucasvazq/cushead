#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from os import path

from PIL import Image
from resizeimage import resizeimage

from .helpers import Errors, FilesHelper, FoldersHelper


class Values:

    def __init__(self):
        __doc__ = """
        Variables:
            names (list)
            brand (obj)
            
        names = [identifier (str)]
            
        brand: {
                identifier: {
                    name_ref (str) Required
                    name (str) Required
                    square_sizes (int list)
                    non_square_sizes (list of int list)
                    file_type (str)
                    title (str)
                    metatag (bool)
                    no_head (bool)
                    verbosity (bool)
                }
            }
        
        identifier: only for identify objects inside brand object
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
        B: <link rel="fluid-icon" href="/static/fluidicon-512x512.png"
            title="Microsoft" />
            
        Template:
        <{} {}='{}' {}{}{}='{}{}' {}/>.format(
            tagname,  # A: link
            attribute,  # A: rel
            name_ref,  # A: shortcut icon
            file_type,  # A: type="image/png"
            sizes,  # A: sizes="16x16"
            ref,  # A: href
            static_url,  # A: /static/
            filename,  # A: favicon-16x16.png
            title,  # B: title="Microsoft"
        )
        
        """

        # Order of how icons are generated and added to the head if it's
        # required
        # The order matters
        self.names = ['icon-sizes', 'apple-touch-icon-default',
                      'apple-touch-icon-sizes', 'apple-touch-startup-image',
                      'windows', 'fluid-icon', 'browserconfig', 'manifest',
                      'opensearch']
        self.brand = {
            'icon-sizes': {
                'name_ref': 'icon',
                'name': 'favicon',
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
                'name': 'ms-icon',
                'square_sizes': [144],
                'metatag': True,
            },
            'apple-touch-icon-default': {
                'name_ref': 'apple-touch-icon',
                'name': 'apple-touch-icon',
                'square_sizes': [57],
            },
            'apple-touch-icon-sizes': {
                'name_ref': 'apple-touch-icon',
                'name': 'apple-touch-icon',
                'square_sizes': [57, 60, 72, 76, 114, 120, 144, 152, 167, 180,
                                 1024],
                'verbosity': True,
            },
            'apple-touch-startup-image': {
                'name_ref': 'apple-touch-startup-image',
                'name': 'launch',
                'square_sizes': [768],
            },
            'fluid-icon': {
                'name_ref': 'fluid-icon',
                'name': 'fluidicon',
                'square_sizes': [512],
                'title': 'Microsoft',
            },
            'browserconfig': {
                'name_ref': 'browserconfig',
                'name': 'ms-icon',
                'square_sizes': [30, 44, 70, 150, 310],
                'non_square_sizes': [[310, 150]],
                'no_head': True,
            },
            'manifest': {
                'name_ref': 'manifest',
                'name': 'android-icon',
                'square_sizes': [36, 48, 72, 96, 144, 192, 256, 384, 512],
                'file_type': 'image/png',
                'no_head': True,
                'verbosity': True,
            },
            'opensearch': {
                'name_ref': 'opensearch',
                'name': 'opensearch',
                'sqyare_sizes': [16],
                'no_head': True,
                'verbosity': True,
            },
        }
        super().__init__()


class Icons:
    brand = None
    config = None
    names = None
    static_folderpath = None

    def __init__(self):
        super().__init__()

    def _icons_head_creator(self, filename, name, size):

        if 'no-head' in self.brand[name]:
            return False

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
            sizes,  # A: sizes="16x16"
            ref,  # A: href
            static_url,  # A: /static/
            filename,  # A: favicon-16x16.png
            title,  # B: title="Microsoft"
        )
        return element

    def _requirements(self, key):
        if key not in self.config:
            return False
        Errors.void_key(self.config[key], key)
        Errors.is_file(self.config[key], key)
        return True

    def favicon_png(self):

        if not self._requirements('favicon_png'):
            return []

        head = []

        # Open favicon_png file
        with open(self.config['favicon_png'], 'r+b') as f, \
                Image.open(f) as image:
            for name in self.names:

                # Resize 'favicon_png' to determinated sizes
                square_sizes = self.brand[name].get('square_sizes', [])
                square_sizes = [[size, size] for size in square_sizes]
                non_square_sizes = self.brand[name].get('non_square_sizes', [])
                sizes = square_sizes + non_square_sizes
                for size in sizes:
                    filename = (f"{self.brand[name]['name']}-"
                                f"{size[0]}x{size[1]}.png")
                    filepath = path.join(self.static_folderpath, filename)
                    self.resize(image, size, filepath)

                    # Some icons need to be added to head
                    element = self._icons_head_creator(filename, name, size)
                    if element:
                        head.append(element)

        return head

    def favicon_ico(self):

        if not self._requirements('favicon_ico'):
            return []

        # Root destination
        source = path.join(os.getcwd(), self.config['favicon_ico'])
        destination = path.join(self.config['files_output'], "favicon.ico")
        FilesHelper.copy_file(source, destination)

        s = ("<link rel='shortcut icon' "
             f"href='/favicon.ico' type='image/x-icon' />")
        return s

    def favicon_svg(self):

        if not self._requirements('favicon_svg'):
            return []

        source = path.join(os.getcwd(), self.config['favicon_svg'])
        destination = path.join(self.static_folderpath, "favicon.svg")
        FilesHelper.copy_file(source, destination)

        color = self.config.get('color', '')
        s = (f"<link rel='mask-icon' href='{self.config['favicon_svg']}' "
             f"color='{color}' />")
        return s

    def preview_png(self):

        if not self._requirements('preview_png'):
            return []

        source = path.join(os.getcwd(), self.config['preview_png'])
        destination = path.join(self.static_folderpath, "preview.png")
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
            for size in self.brand['browserconfig']['square_sizes']
        ])
        s += ''.join([
            "<wide{0}x{1}logo src='{2}{3}-{0}x{1}.png' />".format(
                size[0],
                size[1],
                self.config['static_url'],
                self.brand['browserconfig']['name']
            )
            for size in self.brand['browserconfig']['non_square_sizes']
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
            "\n"
            f"Sitemap: {protocol}{self.config['clear_url']}/sitemap.xml"
            if 'sitemap' in self.config else ''
        )
        s = ("User-agent: *\n"
             "Allow: /\n"
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


class ComplementaryFiles(Values, Icons, Others):
    config = None
    static_folderpath = None

    def __init__(self):
        super().__init__()

    def generate(self):
        head = []

        # Create folder for statics folder
        static_folderpath = f".{self.config['static_url']}"
        static_folderpath = path.join(self.config['files_output'],
                                      static_folderpath)
        static_folderpath = path.join(os.getcwd(), static_folderpath)
        FoldersHelper.create_folder(static_folderpath)
        self.static_folderpath = static_folderpath

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
        filepath = path.join(static_folderpath, 'browserconfig.xml')
        FilesHelper.write_file(filepath, browserconfig_content)

        # manifest.json
        manifest_content, manifest_head = self.manifest()
        head.append(manifest_head)
        filepath = path.join(static_folderpath, 'manifest.json')
        FilesHelper.write_file(filepath, manifest_content)

        # opensearch.xml
        opensearch_content, opensearch_head = self.opensearch()
        head.append(opensearch_head)
        filepath = path.join(static_folderpath, 'opensearch.xml')
        FilesHelper.write_file(filepath, opensearch_content)

        if 'clear_url' in self.config:

            # robots.txt
            robots_content = self.robots()
            filepath = path.join(self.config['files_output'], 'robots.txt')
            FilesHelper.write_file(filepath, robots_content)

            # sitemap.xml
            sitemap_content = self.sitemap()
            filepath = path.join(self.config['files_output'], 'sitemap.xml')
            FilesHelper.write_file(filepath, sitemap_content)

        return head
