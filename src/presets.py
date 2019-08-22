#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate default config"""

import os
from os import path
import shutil
import textwrap

from .helpers import FilesHelper, FoldersHelper


class Presets:
    """Generate presets"""
    args = {}
    info = {}

    def assets(self):
        """Generate images files to attach to the preset settings"""
        filenames = [
            'favicon_ico.ico',
            'favicon_png.png',
            'favicon_svg.svg',
            'presentation_png.png',
        ]
        for filename in filenames:
            # GENERATE BASE64 .png, .ico
            pass

    def settings(self):
        """Generate config file in indented JSON format"""
        string = textwrap.dedent(f"""\
            {{
                'comment':  {{
                    'About':            '{('Config file used by python '
                                           'cushead CLI')}',
                    'Format':           'JSON',
                    'Git':              '{self.info['source']}',
                    'Documentation':    '{self.info['documentation']}'
                }},
                'required': {{
                    'files_output':     '{('./test/tests/Success/'
                                           'complete_config/output')}',
                    'static_url':       '/static/'
                }},
                'recommended': {{
                    'favicon_ico':      './test/tests/favicon-16px.ico',
                    'favicon_png':      './test/tests/favicon-1600px.png',
                    'favicon_svg':      './test/tests/favicon.svg',
                    'preview_png':      './test/tests/preview-500px.png'
                }},
                'default': {{
                    'general': {{
                        'content-type':     'text/html; charset=utf-8',
                        'X-UA-Compatible':  'ie=edge',
                        'viewport':         '{('width=device-width, '
                                               'initial-scale=1')}',
                        'language':         'en',
                        'territory':        'US',
                        'clean_url':        'microsoft.com',
                        'protocol':         'https://',
                        'robots':           'index, follow'
                    }},
                    'basic': {{
                        'title':            'Microsoft',
                        'description':      'Technology Solutions',
                        'subject':          'Home Page',
                        'keywords':         'Microsoft, Windows',
                        'background_color': '#0000FF',
                        'author':           'Lucas Vazquez'
                    }},
                    'social_media': {{
                        'facebook_app_id':  '123456',
                        'twitter_user_@':   '@Microsoft',
                        'twitter_user_id':  '123456'
                    }}
                }},
                'progressive_web_apps': {{
                    'dir':              'ltr',
                    'start_url':        '/',
                    'orientation':      'landscape',
                    'scope':            '/',
                    'display':          'browser',
                    'platform':        'web',
                    'applications':     [
                        {{
                            'platform':     'play',
                            'url':          '{('https://play.google.com/store/'
                                               'apps/details?id=com.example'
                                               '.app')}',
                            'id':           'com.example.app'
                        }},
                        {{
                            'platform':     'itunes',
                            'url':          '{('https://itunes.apple.com/app/'
                                            'example-app/id123456')}'
                        }}
                    ]
                }}
            }}""")
        string = string.replace('\'', '"')
        filepath = path.join(os.getcwd(), self.args.preset)
        folderpath = path.dirname(filepath)
        FoldersHelper.create_folder(folderpath)
        FilesHelper.write_file(filepath, string)
