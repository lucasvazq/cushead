#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import getcwd
from os.path import join
import textwrap


VALUES = """values = {

    # MAIN CONFIG (Required)
    'html_file':        './index.html',
    'output':           './OUTPUT/PATH/', # e.g. for manifest.json
    'static_url':       '/static/',

    # GENERAL CONFIG
    'content-type':     'text/html; charset=utf-8',
    'X-UA-Compatible':  'ie=edge',
    'viewport':         {'width': 'device-width', 'initial-scale': '1'},
    'locale':           'en_US',
    'type':             'website', # http://ogp.me/#types
    'color':            '#FFFFFF',
    'url':              'microsoft.com', # Without "www." and protocol (e.g. "http://")
    'protocol':         'https://',
    'robots':           'index, follow',
    'browserconfig':    'browserconfig.xml',
    'manifest':         'manifest.json',
    'opensearch':       'opensearch.xml',
    'sitemap':          'sitemap.xml',

    # BASIC CONFIG
    'title':            'Microsoft',
    'description':      'Technology Solutions',
    'subject':          'Home Page',
    'keywords':         'Microsoft, Windows',

    # IMAGES
    # If icon_png is specified, the file must be exists.
    'preview':          'preview.png', # Big image preview
    'preview_type':     'image/png', # image/jpeg, image/gif or image/png
    'icon':             'favicon.ico', # *.ico
    'icon_png':         'favicon.png', # FILEPATH PNG IMAGE 512x512
    'mask-icon':        'maskicon.svg', # svg file type

    # SOCIAL MEDIA
    'fb:app_id':        '12345', # Facebook App ID
    'tw:site':          '@Microsoft', # Twitter account
    'tw:creator:id':    '123456', # Page editor ID

    # PWA
    'dir':              'ltr',
    'start_url':        '/',
    'orientation':      'landscape',
    'scope':            '/',
    'display':          'browser',
    'platform':        'web',
    'applications':     [
        {
            'platform': 'play',
            'url':      'https://play.google.com/store/apps/details?id=com.example.app',
            'id':       'com.example.app'
        },
        {
            'platform': 'itunes',
            'url':      'https://itunes.apple.com/app/example-app/id123456',
        }
    ],

    # AUTHOR
    'author':           'Lucas Vazquez'

}"""


class Presets():

    def __init__(self):
        self.presets = VALUES
        super().__init__()

    def _make_preset(self, file):
        file = join(getcwd(), file)
        f = open(file, 'w+')
        f.write(self.presets)
        f.close()
        print(textwrap.dedent("""\
            PRESET:
            {}""".format(self.presets)))
