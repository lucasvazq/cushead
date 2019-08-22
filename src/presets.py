#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate default config"""

import os
from os import path
import textwrap

from .helpers import FilesHelper, FoldersHelper


def make_preset(file, info):
    """Generate config in indented JSON format"""
    string = textwrap.dedent(f"""\
        {{
            'comment':  {{
                'About':            '{('Config file used by python '
                                       'cushead CLI')}',
                'Format':           'JSON',
                'Git':              '{info['source']}',
                'Documentation':    '{info['documentation']}'
            }},
            'required': {{
                'files_output':     '{('./test/tests/Success/'
                                       'complete_config/wasa')}',
                'static_url':       '/static/wasa'
            }},
            'recommended': {{
                'favicon_png':      './test/tests/favicon.png',
                'favicon_ico':      './test/tests/favicon.ico',
                'favicon_svg':      './test/tests/favicon.svg',
                'preview_png':      './test/tests/preview.png'
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
                    'background_color': '#FFFFFF',
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
    filepath = path.join(os.getcwd(), file)
    folderpath = path.dirname(filepath)
    FoldersHelper.create_folder(folderpath)
    FilesHelper.write_file(filepath, string)
