#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This simple script improve your SEO and UX.
It add lang attribute to the html element and search and replace '$head$' string with personalized head elements.

Git repository:
    https://github.com/lucasvazq/cushead.py
'''

import sys

if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')

import json
import types
from configparser import ConfigParser
from importlib import machinery
from os import fdopen, getcwd, path, remove
from shutil import move
from tempfile import mkstemp

import argparse


def parameters():

    parser = argparse.ArgumentParser(
        usage='cushead.py -file PATH/TO/FILE [--exclude-html, ..]',
        description='This simple script improve your SEO and UX. ' + 
            'It add lang attribute to the <html> element and search and replace \'$head$\' string with personalized head elements. ' +
            'Git repository: https://github.com/mrsantos321/cushead .')

    parser._action_groups.pop()
    helpers = parser.add_argument_group('help')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    helpers.add_argument('-presset', metavar=('FILENAME'), dest='presset', help='Generate example file with pressets.')

    required.add_argument('-file', metavar=('FILEPATH'), dest='file', help='Path to file that want to edit.')

    optional.add_argument('--exclude-comment', dest='comment', action='store_false', help='Exclude \'Custom head elements\' comment.')
    optional.add_argument('--exclude-html', dest='html', action='store_false', help='Exclude html lang attribute.')
    optional.add_argument('--exclude-config', dest='basic_config', action='store_false', help='Exclude basic head config elements.')
    optional.add_argument('--exclude-seo', dest='basic_seo', action='store_false', help='Exclude basic SEO elements.')
    optional.add_argument('--exclude-opengraph', dest='opengraph', action='store_false', help='Exclude opengraph.')
    optional.add_argument('--exclude-facebook', dest='facebook', action='store_false', help='Exclude facebook.')
    optional.add_argument('--exclude-twitter', dest='twitter', action='store_false', help='Exclude twitter.')
    optional.add_argument('--exclude-author', dest='author', action='store_false', help='Exclude author.')
    parser.set_defaults(comment=True)
    parser.set_defaults(html=True)
    parser.set_defaults(basic_config=True)
    parser.set_defaults(basic_seo=True)
    parser.set_defaults(opengraph=True)
    parser.set_defaults(facebook=True)
    parser.set_defaults(twitter=True)
    parser.set_defaults(author=True)

    parser = parser.parse_args()

    if not (parser.presset or parser.file):
        raise Exception('Miss -file argument. Can do \'cushead.py -h\' for help.')
    if parser.presset and parser.file:
        raise Exception('Cant use -presset and -file arguments together. Can do \'cushead.py -h\' for help.')
    if parser.file:
        if not path.isfile(parser.file):
            raise Exception('Argument passed by -file (' + str(parser.file) + ') can\'t be found.')

    return parser


def make_presset(file):

    file = path.join(getcwd(), file)
    f = open(file, 'w+')
    values = '''values = {

    # FILE PATH
    'path':             './index.html',

    # BASIC CONFIG
    'content-type':     'text/html; charset=utf-8',
    'X-UA-Compatible':  'ie=edge',
    'robots':           'index, follow',
    'manifest':         '/manifest.json',
    'msapp-config':     '/browserconfig.xml',
    'viewport':         {'width': 'device-width', 'initial-scale': '1'},
    'locale':           'en_US',

    # BASIC SEO
    'title':            'Microsoft',
    'description':      'Technology Solutions',
    'icon':             '/static/favicon.png',
    'subject':          'Home Page',
    'keywords':         'Microsoft, Windows',

    # SOCIAL MEDIA

    # General
    'preview':          '/static/preview.png', # Big image preview

    # Opengraph
    # og:title, og:description, og:image, og:image:secure_url and og:locale obtained
    # from BASIC SEO and BASIC CONFIG sections.
    'og:url':            'www.microsoft.com',
    'og:type':          'website', # http://ogp.me/#types
    'og:image:type':    'image/png', # image/jpeg, image/gif or image/png

    # Facebook
    'fb:app_id':        '12345', # (Str) Facebook App ID

    # Twitter
    # Only support twitter:card = summary
    # twitter:title, twitter:description, twitter:image and twitter:image:alt
    # obtained from BASIC SEO and General - SOCIAL MEDIA sections.
    'tw:site':          '@Microsoft', # Commerce Twitter account
    'tw:creator:id':    '123456', # Page editor ID
    
    # AUTHOR
    'author':           'Lucas Vazquez'
    
}'''

    f.write(values)
    f.close()
    print('\nPRESSET:\n' +
        values + '\n')

def get_values(file):

    name = file
    file = path.join(getcwd(), file)

    loader = machinery.SourceFileLoader(name, file)
    mod = types.ModuleType(loader.name)
    loader.exec_module(mod)

    return mod.values


def add_basic_config(dictionary, temp):
    # content-type
    if 'content-type' in dictionary:
        if len(dictionary['content-type']):
            temp.append('<meta http-equiv="Content-Type" content="' + dictionary['content-type'] + '" />')
    # x-ua-compatible
    if 'X-UA-Compatible' in dictionary:
        if len(dictionary['X-UA-Compatible']):
            temp.append('<meta http-equiv="X-UA-Compatible" content="' + dictionary['X-UA-Compatible'] + '" />')
    # robots
    if 'robots' in dictionary:
        if len(dictionary['robots']):
            temp.append('<meta name="robots" content="' + dictionary['robots'] + '" />')
    # manifest
    if 'manifest' in dictionary:
        if len(dictionary['X-UA-Compatible']):
            temp.append('<link rel="manifest" href="' + dictionary['manifest'] + '" />')
    # msapplication-config
    if 'msapp-config' in dictionary:
        if len(dictionary['msapp-config']):
            temp.append('<meta name="msapplication-config" content="' + dictionary['msapp-config'] + '" />')
    # viewport
    if 'viewport' in dictionary:
        if len(dictionary['viewport']):
            concat = ''
            for x in dictionary['viewport']:
                concat += str(x) + '=' + str(dictionary['viewport'][x]) + ', '
            concat = concat[0:-2]
            temp.append('<meta name="viewport" content="' + concat + '" />')
    # locale
    if 'locale' in dictionary:
        if len(dictionary['locale']):
            temp.append('<meta http-equiv="Content-Language" content="' + dictionary['locale'] + '" />')

    return temp


def add_basic_seo(dictionary, temp):

    # title
    if 'title' in dictionary:
        if len(dictionary['title']):
            temp.append('<title>' + dictionary['title'] + '</title>')
    # description
    if 'description' in dictionary:
        if len(dictionary['description']):
            temp.append('<meta name="description" content="' + dictionary['description'] + '" />')
    # icon
    if 'icon' in dictionary:
        if len(dictionary['icon']):
            temp.append('<link rel="shortcut icon" href="' + dictionary['icon'] + '" />')
    # subject
    if 'subject' in dictionary:
        if len(dictionary['subject']):
            temp.append('<meta name="subject" content="' + dictionary['subject'] + '" />')
    # keywords
    if 'keywords' in dictionary:
        if len(dictionary['keywords']):
            temp.append('<meta name="keywords" content="' + dictionary['keywords'] + '" />')
            

    return temp


def add_opengraph(dictionary, temp):

    '''Special'''

    # og:locale
    if 'locale' in dictionary:
        if len(dictionary['locale']):
            temp.append('<meta property="og:locale" content="' + dictionary['locale'] + '" />')
    # og:type
    if 'og:type' in dictionary:
        if len(dictionary['og:type']):
            temp.append('<meta property="og:type" content="' + dictionary['og:type'] + '" />')
    # og:url, Likes and Shared are stored under this url
    if 'og:url' in dictionary:
        if len(dictionary['og:url']):
            temp.append('<meta property="og:url" content="' + dictionary['og:url'] + '" />')

    '''Preview'''

    # og:site_name
    if 'title' in dictionary:
        if len(dictionary['title']):
            temp.append('<meta property="og:site_name" content="' + dictionary['title'] + '" />')
    # og:title
    if 'title' in dictionary:
        if len(dictionary['title']):
            temp.append('<meta property="og:title" content="' + dictionary['title'] + '" />')
    # og:description
    if 'description' in dictionary:
        if len(dictionary['description']):
            temp.append('<meta property="og:description" content="' + dictionary['description'] + '" />')
    # og:image (http) and og:image:secure_url (https)
    if 'preview' in dictionary or 'icon' in dictionary:
        if 'preview' in dictionary:
            if len(dictionary['preview']):
                temp.append('<meta property="og:image" content="' + dictionary['preview'] + '" />')
                temp.append('<meta property="og:image:secure_url" content="' + dictionary['preview'] + '" />')
            elif len(dictionary['icon']):
                temp.append('<meta property="og:image" content="' + dictionary['icon'] + '" />')
                temp.append('<meta property="og:image:secure_url" content="' + dictionary['icon'] + '" />')
        else:
            if len(dictionary['icon']):
                temp.append('<meta property="og:image" content="' + dictionary['icon'] + '" />')
                temp.append('<meta property="og:image:secure_url" content="' + dictionary['icon'] + '" />')
    # og:image:type
    if 'og:image:type' in dictionary:
        temp.append('<meta property="og:image:type" content="' + dictionary['og:image:type'] + '" />')
    # og:image:alt
    if 'title' or 'description' in dictionary:
        if len(dictionary['title']):
            title = dictionary['title']
        else:
            title = ''
        if len(dictionary['description']):
            description = dictionary['description']
        else:
            description = ''
        if 'title' and 'description' in dictionary:
            connector = ' - '
        else:
            connector = ''
        text = title + connector + description
        temp.append('<meta name="og:image:alt" content="' + text + '" />')
    
    return temp


def add_facebook(dictionary, temp):

    '''App'''

    # fb:app_id
    if 'fb:app_id' in dictionary:
        if len(dictionary['fb:app_id']):
            temp.append('<meta porperty="fb:app_id" content="' + dictionary['fb:app_id'] + '" />')

    return temp


def add_twitter(dictionary, temp):

    '''Required'''

    temp.append('<meta name="twitter:card" content="summary">')

    '''Preview'''

    # twitter:site
    if 'tw:site' in dictionary:
        if len(dictionary['tw:site']):
            temp.append('<meta name="twitter:site" content="' + dictionary['tw:site'] + '" />')
    # twitter:title
    if 'title' in dictionary:
        if len(dictionary['title']):
            temp.append('<meta name="twitter:title" content="' + dictionary['title'] + '" />')
    # twitter:description
    if 'description' in dictionary:
        if len(dictionary['description']):
            temp.append('<meta name="twitter:description" content="' + dictionary['description'] + '" />')
    # twitter:image
    if 'preview' in dictionary or 'icon' in dictionary:
        if 'preview' in dictionary:
            if len(dictionary['preview']):
                temp.append('<meta name="twitter:image" content="' + dictionary['preview'] + '" />')
            elif len(dictionary['icon']):
                temp.append('<meta name="twitter:image" content="' + dictionary['icon'] + '" />')
        else:
            if len(dictionary['icon']):
                temp.append('<meta name="twitter:image" content="' + dictionary['icon'] + '" />')
    # twitter:image:alt
    if 'title' or 'description' in dictionary:
        if len(dictionary['title']):
            title = dictionary['title']
        else:
            title = ''
        if len(dictionary['description']):
            description = dictionary['description']
        else:
            description = ''
        if 'title' and 'description' in dictionary:
            connector = ' - '
        else:
            connector = ''
        text = title + connector + description
        temp.append('<meta name="twitter:image:alt" content="' + text + '" />')
    # tw:creator
    if 'tw:creator:id' in dictionary:
        if len(dictionary['tw:creator:id']):
            temp.append('<meta property="twitter:creator:id" content="' + dictionary['tw:creator:id'] + '" />')

    return temp


def add_author(dictionary, temp):

    # author
    if 'author' in dictionary:
        if len(dictionary['author']):
            temp.append('<meta name="author" content="' + dictionary['author'] + '" />')

    return temp


def cushead():

    args = parameters()

    if args.presset:
        
        make_presset(args.presset)

        print('PATH: ' + args.presset)
        print('FULLPATH: ' + path.join(getcwd(), args.presset))

    else:

        dictionary = get_values(args.file)

        if not len(dictionary['path']):
            raise Exception('Miss \'path\' element on -file ' + args.file + ' and its required.')

        temp = []
        if args.basic_config:
            temp = add_basic_config(dictionary, temp)
        if args.basic_seo:
            temp = add_basic_seo(dictionary, temp)
        if args.opengraph:
            temp = add_opengraph(dictionary, temp)
        if args.facebook:
            temp = add_facebook(dictionary, temp)
        if args.twitter:
            temp = add_twitter(dictionary, temp)
        if args.author:
            temp = add_author(dictionary, temp)

        success = False

        # Read contents from file as a single string
        file_handle = open(dictionary['path'], 'r')
        file_string = file_handle.read()
        file_handle.close()

        # Generate idented dom
        space = file_string.split('$head$')
        if '$head$' in file_string:
            space = space[0].split('\n')
            space = space[len(space) - 1]
            if args.comment:
                concat = '<!-- Custom head elements -->\n'
            else:
                concat = ''
            for x in temp:
                concat += space + x + '\n'
            concat = concat[0:-1]

        # Add lang attribute to <html>
        if len(dictionary['locale']):
            if not '<html>' in file_string:
                print('Miss <html>, cant add lang attribute')
            else:
                file_string = file_string.replace('<html>', '<html lang="' + dictionary['locale'] + '">')
                print('\nHTML:\n' +
                    '<html lang="' + dictionary['locale'] + '">')

        # Add custom head elements
        if not '$head$' in file_string:
            print('Miss $head$, cant add custom elements')
        else:
            file_string = file_string.replace('$head$', concat)
            print('\nHEAD:\n' +
                concat)

        # Write contents to file.
        # Using mode 'w' truncates the file.
        file_handle = open(dictionary['path'], 'w')
        file_handle.write(file_string)
        file_handle.close()

        print('\nPATH: ' + dictionary['path'])
        print('FULLPATH: ' + path.join(getcwd(), dictionary['path']))

    print('\nDone')

cushead()
