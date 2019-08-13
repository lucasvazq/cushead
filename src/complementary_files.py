#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import json
from os import getcwd
from os.path import isfile, join

from resizeimage import resizeimage

from .helpers import Helpers


class Values():

    def __init__(self):
        self.names = ['icon-sizes', 'windows', 'apple-touch-icon-default',
            'apple-touch-icon-sizes', 'fluid-icon', 'manifest', 'browserconfig']
        self.brand = {
            'icon-sizes': {
                'name_ref': 'icon',
                'name': 'favicon',
                # https://www.favicon-generator.org/
                # https://stackoverflow.com/questions/4014823/does-a-favicon-have-to-be-32x32-or-16x16
                # https://www.emergeinteractive.com/insights/detail/the-essentials-of-favicons/
                'sizes' : [16, 24, 32, 48, 57, 60, 64, 70, 72, 76, 96, 114, 120, 128, 144, 150,
                    152, 167, 180, 192, 195, 196, 228, 310],
                'verbosity': True,
                'type': 'image/png',
            },
            'windows': {
                'name_ref': 'msapplication-TileImage',
                'name': 'ms-icon',
                'sizes': [144],
                'metatag': True
            },
            'apple-touch-icon-default': {
                'name_ref': 'apple-touch-icon',
                'name': 'apple-touch-icon',
                'sizes': [57],
            },
            'apple-touch-icon-sizes': {
                'name_ref': 'apple-touch-icon',
                'name': 'apple-touch-icon',
                'sizes': [57, 60, 72, 76, 114, 120, 144, 152, 180],
                'verbosity': True,
            },
            'fluid-icon': {
                'name_ref': 'fluid-icon',
                'name': 'fluidicon',
                'sizes': [512],
                'title': 'Microsoft'
            },
            'manifest': {
                'name_ref': 'manifest',
                'name': 'android-icon',
                'sizes' : [36, 48, 72, 96, 144, 192],
                'verbosity': True,
                'type': 'image/png',
                'no-head': True
            },
            'browserconfig': {
                'name_ref': 'browserconfig',
                'name': 'ms-icon',
                'sizes': [30, 44, 70, 150, 310],
                'special_sizes': [[310, 150]],
                'no-head': True
            }
        }


class Icons():

    def __init__(self, dictionary=None):
        self.values = dictionary

    def _resize(self, image, size, filename):
        filepath = join(self.values['output'], filename)
        cover = resizeimage.resize_contain(image, [size[0], size[1]])
        cover.save(join(self.values['output'], filename), image.format)
        return filepath

    def general_icons(self, name, size, filename):
        if 'no-head' in self.brand[name]:
            return None
        verbosity = "sizes='{}x{}' ".format(str(size[0]), str(size[1])) \
            if 'verbosity' in self.brand[name] else ''
        (tagname, attribute, ref) = ('meta', 'name', 'content') \
            if 'metatag' in self.brand[name] else \
            ('link', 'rel', 'href')
        file_type = 'type="{}" '.format(self.brand[name]['type']) \
            if 'type' in self.brand[name] else ''
        title = "title='{}' ".format(self.brand[name]['title']) \
            if 'title' in self.brand[name] else ''
        # A: <link rel="shortcut icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png" />
        # B: <link rel="fluid-icon" href="/static/fluidicon-512x512.png" title="Microsoft" />
        name_ref = self.brand[name]['name_ref']
        static_url = self.values['static_url']
        element = "<{} {}='{}' {}{}{}='{}{}' {}/>".format(
                tagname,    # A: link
                attribute,  # A: rel
                name_ref,   # A: shortcut icon
                file_type,  # A: type="image/png"
                verbosity,  # A: sizes="16x16"
                ref,        # A: href
                static_url, # A: /static/
                filename,   # A: favicon-16x16.png
                title       # B: title="Microsoft"
            )
        return element

    def icon(self):
        if 'icon' in self.values:
            return ("<link rel='shortcut icon' href='{}' type='image/x-icon' />".format(
                self.values['icon']))

    def mask_icon(self):
        if 'mask-icon' in self.values:
            color = self.values.get('color', '')
            return ("<link rel='mask-icon' href='{}' color='{}' />".format(
                    self.values['mask-icon'], color))


class Others():

    def __init__(self, dictionary=None):
        self.values = dictionary

    def browserconfig(self):
        string = ("<?xml version='1.0' encoding='utf-8'?><browserconfig>" +
            "<msapplication><tile>")
        string += ''.join([
            "<square{0}x{0}logo src='{1}{2}-{0}x{0}.png' />".format(
                size, self.values['static_url'], self.brand['browserconfig']['name'])
            for size in self.brand['browserconfig']['sizes']])
        string += ''.join([
            "<wide{0}x{1}logo src='{2}{3}-{0}x{1}.png' />".format(
                size[0], size[1], self.values['static_url'],
                self.brand['browserconfig']['name'])
            for size in self.brand['browserconfig']['special_sizes']])
        color = self.values.get('color', '')
        string += ("<TileColor>{}</TileColor></tile></msapplication></browserconfig>"
            .format(color))
        return [string.replace('\'', '"'), ("<meta name='msapplication-config' " +
            "content='{}' />".format(self.values['browserconfig']))]

    def manifest(self):
        path = self.values['static_url'].replace('/', '\/')
        icons = [{
            'src': "{0}{1}-{2}x{2}".format(path, self.brand['manifest']['name'],
                str(size)),
            'sizes': "{0}x{0}".format(str(size)),
            'type': 'image\/png',
            'density': str(size/48)}
            for size in self.brand['manifest']['sizes']]
        dictionary = {}
        if 'title' in self.values:
            dictionary['title'] = self.values['title']
            dictionary['short_name'] = self.values['title']
        if 'description' in self.values:
            dictionary['description'] = self.values['description']
        if 'dir' in self.values:
            dictionary['dir'] = self.values['dir']
        if 'start_url' in self.values:
            dictionary['start_url'] = self.values['start_url']
        if 'orientation' in self.values:
            dictionary['orientation'] = self.values['orientation']
        if 'color' in self.values:
            dictionary['background_color'] = self.values['color']
            dictionary['theme_color'] = self.values['color']
        if 'lang' in self.values:
            dictionary['lang'] = self.values['lang']
        if 'scope' in self.values:
            dictionary['scope'] = self.values['scope']
        if 'display' in self.values:
            dictionary['display'] = self.values['display']
        if 'plataform' in self.values:
            dictionary['platform'] = self.values['plataform']
        if 'applications' in self.values:
            dictionary['related_applications'] = self.values['applications']
        dictionary['icons'] = icons
        return [json.dumps(dictionary).replace('\\\\', '\\'),
            "<link rel='manifest' href='{}' />".format(self.values['manifest'])]

    def opensearch(self):
        title = self.values.get('title', '')
        url = self.values.get('url', '')
        content = ("<?xml version='1.0' encoding='utf-8'?>" +
            "<OpenSearchDescription xmlns:moz='" +
            "http://www.mozilla.org/2006/browser/search/' " +
            "xmlns='http://a9.com/-/spec/opensearch/1.1/'>" +
            "<ShortName>{0}</ShortName>" +
            "<Description>Search {0}</Description>" +
            "<InputEncoding>UTF-8</InputEncoding>" +
            "<Url method='get' type='text/html' " +
            "template='http://www.google.com/search?q=" +
            "{{searchTerms}}+site%3A{1}' />" +
            "</OpenSearchDescription>".format(title, url))
        return [content.replace('\'', '"'), ("<link rel='search' " +
            "type='application/opensearchdescription+xml' title='{}' href='{}' />".format(
                title, self.values['opensearch']))]

    def robots(self):
        string = ("User-agent: *" +
            "Allow: /" +
            "\\" +
            "Sitemap: {}{}/{}".format(self.values.get('protocol', ''),
                self.values['url'], self.values['sitemap']))
        return string

    def sitemap(self):
        return ("<?xml version='1.0' encoding='uft-8'?>" +
            "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9' " +
	        "xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' " +
	        "xsi:schemaLocation='http://www.sitemaps.org/schemas/sitemap/0.9 " +
            "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'>" +
            "<url><loc>{}{}/</loc></url></urlset>""".format(
                self.values.get('protocol', ''), self.values['url'])).replace('\'', '"')


class ComplementaryFiles(Values, Icons, Others):

    def __init__(self, dictionary=None):
        self.values = dictionary
        Values.__init__(self)
        Icons.__init__(self)
        Others.__init__(self)

    def generate(self):
        head = []
        if 'icon_png' in self.values and 'static_url' in self.values:
            if not isfile(self.values['icon_png']):
                raise Exception("Missing file passed by icon_png key value ({})".format(
                    join(getcwd(), self.values['icon_png'])))
            new_files = []
            with open(self.values['icon_png'], 'r+b') as f:
                with Image.open(f) as image:
                    for name in self.names:
                        for size in self.brand[name].get('sizes', []):
                            filename = "{0}-{1}x{1}.png".format(self.brand[name]['name'], str(size))
                            new_files.append(self._resize(image, [size, size], filename))
                            element = self.general_icons(name, [size, size], filename)
                            if element:
                                head.append(element)
                        for size in self.brand[name].get('special_sizes', []):
                            filename = "{}-{}x{}.png".format(self.brand[name]['name'], str(size[0]),
                                str(size[1]))
                            new_files.append(self._resize(image, size, filename))
                            element = self.general_icons(name, size, filename)
                            if element:
                                head.append(element)
            element = self.icon()
            if element:
                head.append(element)
            element = self.mask_icon()
            if element:
                head.append(element)
            if 'browserconfig' in self.values:
                browserconfig_content, browserconfig_head = self.browserconfig()
                head.append(browserconfig_head)
                new_files.append(self._write_file(join(self.values['output'],
                    self.values['browserconfig']), browserconfig_content))
            if 'manifest' in self.values:
                manifest_content, manifest_head = self.manifest()
                head.append(manifest_head)
                new_files.append(self._write_file(join(self.values['output'],
                    self.values['manifest']), manifest_content))
            if 'opensearch' in self.values:
                opensearch_content, opensearch_head = self.opensearch()
                head.append(opensearch_head)
                new_files.append(self._write_file(join(self.values['output'],
                    'opensearch.xml'), opensearch_content))
            if 'url' in self.values:
                new_files.append(self._write_file(join(self.values['output'],
                    'robots.txt'), self.robots()))
            if 'url' in self.values and 'sitemap' in self.values:
                new_files.append(self._write_file(join(self.values['output'],
                    self.values['sitemap']), self.sitemap()))
        return head, new_files
