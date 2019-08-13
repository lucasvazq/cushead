#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import json
from os import getcwd, path
from textwrap import dedent

from resizeimage import resizeimage


class Values():

    def __init__(self):
        self.names = ['icon-sizes', 'windows', 'apple-touch-icon-default',
            'apple-touch-icon-sizes', 'fluid-icon', 'browserconfig', 'manifest',
            'opensearch']
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
            'browserconfig': {
                'name_ref': 'browserconfig',
                'name': 'ms-icon',
                'sizes': [30, 44, 70, 150, 310],
                'special_sizes': [[310, 150]],
                'no-head': True
            },
            'manifest': {
                'name_ref': 'manifest',
                'name': 'android-icon',
                'sizes' : [36, 48, 72, 96, 144, 192],
                'verbosity': True,
                'type': 'image/png',
                'no-head': True
            },
            'opensearch': {
                'name_ref': 'opensearch',
                'name': 'opensearch',
                'sizes': [16],
                'verbosity': True,
                'no-head': True
            }
        }
        super().__init__()


class Icons():

    def __init__(self):
        super().__init__()

    def _resize(self, image, size, filename):
        filepath = path.join(self.config['output'], filename)
        cover = resizeimage.resize_contain(image, [size[0], size[1]])
        cover.save(path.join(self.config['output'], filename), image.format)
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
        static_url = self.config['static_url']
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
        if 'icon' in self.config:
            return ("<link rel='shortcut icon' href='{}{}' type='image/x-icon' />".format(
                self.config['static_url'], self.config['icon']))

    def mask_icon(self):
        if 'mask-icon' in self.config:
            color = self.config.get('color', '')
            return ("<link rel='mask-icon' href='{}' color='{}' />".format(
                    self.config['mask-icon'], color))


class Others():

    def __init__(self):
        super().__init__()

    def browserconfig(self):
        string = ("<?xml version='1.0' encoding='utf-8'?><browserconfig>" +
            "<msapplication><tile>")
        string += ''.join([
            "<square{0}x{0}logo src='{1}{2}-{0}x{0}.png' />".format(
                size, self.config['static_url'], self.brand['browserconfig']['name'])
            for size in self.brand['browserconfig']['sizes']])
        string += ''.join([
            "<wide{0}x{1}logo src='{2}{3}-{0}x{1}.png' />".format(
                size[0], size[1], self.config['static_url'],
                self.brand['browserconfig']['name'])
            for size in self.brand['browserconfig']['special_sizes']])
        color = self.config.get('color', '')
        string += ("<TileColor>{}</TileColor></tile></msapplication></browserconfig>"
            .format(color))
        return [string.replace('\'', '"'), ("<meta name='msapplication-config' " +
            "content='{}{}' />".format(self.config['static_url'],
                self.config['browserconfig']))]

    def manifest(self):
        path = self.config['static_url']
        icons = [{
            'src': "{0}{1}-{2}x{2}".format(path, self.brand['manifest']['name'],
                str(size)),
            'sizes': "{0}x{0}".format(str(size)),
            'type': 'image/png',
            'density': str(size/48)}
            for size in self.brand['manifest']['sizes']]
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
        if 'locale' in self.config:
            dictionary['locale'] = self.config['locale']
        if 'scope' in self.config:
            dictionary['scope'] = self.config['scope']
        if 'display' in self.config:
            dictionary['display'] = self.config['display']
        if 'platform' in self.config:
            dictionary['platform'] = self.config['platform']
        if 'applications' in self.config:
            dictionary['related_applications'] = self.config['applications']
        dictionary['icons'] = icons
        return [json.dumps(dictionary), "<link rel='manifest' href='{}{}' />".format(
            self.config['static_url'], self.config['manifest'])]

    def opensearch(self):
        content = ("<?xml version='1.0' encoding='utf-8'?>" +
            "<OpenSearchDescription xmlns:moz='" +
            "http://www.mozilla.org/2006/browser/search/' " +
            "xmlns='http://a9.com/-/spec/opensearch/1.1/'>" +
            "<ShortName>{}</ShortName>".format(self.config.get('title', '')) +
            "<Description>Search {}</Description>".format(self.config.get(
                'title', '')) +
            "<InputEncoding>UTF-8</InputEncoding>" +
            "<Url method='get' type='text/html' " +
            "template='http://www.google.com/search?q=" +
            "{{searchTerms}}+site%3A{}' />".format(self.config.get('url', '')) +
            "<Image height='16' width='16' type='image/png'>" +
            "{}opensearch-16x16.png".format(self.config['static_url']) +
            "</Image>" +
            "</OpenSearchDescription>")
        return [content.replace('\'', '"'), ("<link rel='search' " +
            "type='application/opensearchdescription+xml' title='{}' href='{}{}' />"
                .format(self.config.get('title', ''), self.config['static_url'],
                    self.config['opensearch']))]

    def robots(self):
        string = ("User-agent: *\n" +
            "Allow: /\n" +
            "\n" +
            "Sitemap: {}{}/{}".format(self.config.get('protocol', ''),
                self.config['url'], self.config['sitemap']))
        return string

    def sitemap(self):
        return ("<?xml version='1.0' encoding='uft-8'?>" +
            "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9' " +
	        "xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' " +
	        "xsi:schemaLocation='http://www.sitemaps.org/schemas/sitemap/0.9 " +
            "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'>" +
            "<url><loc>{}{}/</loc></url></urlset>""".format(
                self.config.get('protocol', ''), self.config['url'])).replace('\'', '"')


class ComplementaryFiles(Values, Icons, Others):

    def __init__(self):
        super().__init__()

    def generate(self):
        (head, new_files) = ([], [])
        if 'icon_png' in self.config and 'static_url' in self.config:
            if not len(self.config['icon_png']):
                # test: test_void_icon_png
                raise Exception("'icon_png' key value can't be void.")
            if not path.isfile(self.config['icon_png']):
                # test: test_icon_png_doesnt_exists
                raise Exception(dedent("""\
                    'icon_png' key ({}) must be referred to a file path that exists.
                    FILE PATH: {}""".format(self.config['icon_png'],
                        path.join(getcwd(), self.config['icon_png']))))
            with open(self.config['icon_png'], 'r+b') as f:
                with Image.open(f) as image:
                    for name in self.names:
                        for size in self.brand[name].get('sizes', []):
                            filename = "{0}-{1}x{1}.png".format(self.brand[name]['name'], str(size))
                            new_files.append(self._resize(image, [size, size], filename))
                            # Some square icons are added to head
                            # Can return a String
                            element = self.general_icons(name, [size, size], filename)
                            if element:
                                head.append(element)
                        for size in self.brand[name].get('special_sizes', []):
                            filename = "{}-{}x{}.png".format(self.brand[name]['name'], str(size[0]),
                                str(size[1]))
                            new_files.append(self._resize(image, size, filename))
                            # Non square icons aren't added to head
                            # Returns always None
                            self.general_icons(name, size, filename)
            element = self.icon()
            if element:
                head.append(element)
            element = self.mask_icon()
            if element:
                head.append(element)
            if 'browserconfig' in self.config:
                browserconfig_content, browserconfig_head = self.browserconfig()
                head.append(browserconfig_head)
                new_files.append(self._write_file(path.join(self.config['output'],
                    self.config['browserconfig']), browserconfig_content))
            if 'manifest' in self.config:
                manifest_content, manifest_head = self.manifest()
                head.append(manifest_head)
                new_files.append(self._write_file(path.join(self.config['output'],
                    self.config['manifest']), manifest_content))
            if 'opensearch' in self.config:
                opensearch_content, opensearch_head = self.opensearch()
                head.append(opensearch_head)
                new_files.append(self._write_file(path.join(self.config['output'],
                    'opensearch.xml'), opensearch_content))
            if 'url' in self.config:
                new_files.append(self._write_file(path.join(self.config['output'],
                    'robots.txt'), self.robots()))
            if 'url' in self.config and 'sitemap' in self.config:
                new_files.append(self._write_file(path.join(self.config['output'],
                    self.config['sitemap']), self.sitemap()))
        return head, new_files
