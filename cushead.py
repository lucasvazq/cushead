#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This simple script improve your SEO and UX.
It add lang attribute to the html element and search and replace '$head$' string with personalized head elements.

Git repository:
    https://github.com/mrsantos321/cushead
'''


import json
import sys
import types
from configparser import ConfigParser
from importlib import machinery
from os import fdopen, getcwd, path, remove
from shutil import move
from tempfile import mkstemp

import argparse

if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


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
    optional.add_argument('--exclude-special', dest='special', action='store_false', help='Exclude special head elements.')
    optional.add_argument('--exclude-basic', dest='basic', action='store_false', help='Exclude basic SEO elements.')
    optional.add_argument('--exclude-opengraph', dest='opengraph', action='store_false', help='Exclude opengraph.')
    optional.add_argument('--exclude-facebook', dest='facebook', action='store_false', help='Exclude facebook.')
    optional.add_argument('--exclude-twitter', dest='twitter', action='store_false', help='Exclude twitter.')
    optional.add_argument('--exclude-author', dest='author', action='store_false', help='Exclude author.')
    parser.set_defaults(comment=True)
    parser.set_defaults(html=True)
    parser.set_defaults(special=True)
    parser.set_defaults(basic=True)
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

    # File path
    'path':             './index.html',

    # Basic SEO
    'title':            'Microsoft',
    'icon':             '/favicon.png',
    'preview':          '/preview.png', # Big image preview
    'description':      'Technology Solutions',
    'subject':          'Home Page',
    'keywords':         'Microsoft, Windows',

    # Opengraph
    'og:type':          'website', # http://ogp.me/#types

    # Facebook
    'fb:pages':         {'12345', '67890'}, # (Str) Facebook Pages ID separated by commas
    'fb:app_id':        '12345', # (Str) Facebook App ID

    # Twitter
    'tw:card':          'summary', # https://developer.twitter.com/en/docs/tweets/optimize-with-cards/overview/summary.html
    'tw:domain':        'www.microsoft.com',
    'tw:page':          '@Microsoft', # Commerce Twitter account
    'tw:creator':       '@BillGates', # This page editor
    'tw:googleplay':    '12345', # Google Play app id
    'tw:ipad':          '12345', # iPad app id
    'tw:iphone':        '12345', # iPhone app id

    # Other
    'content-type':     'text/html; charset=utf-8',
    'viewport':         {'width': 'device-width', 'initial-scale': '1'},
    'locale':           'en_US',

    # Website author
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


def add_special(dictionary, temp):

    # content-type
    if 'content-type' in dictionary:
        if len(dictionary['content-type']):
            temp.append('<meta http-equiv="Content-Type" content="' + dictionary['content-type'] + '" />')
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


def add_basic(dictionary, temp):

    # title
    if 'title' in dictionary:
        if len(dictionary['title']):
            temp.append('<title>' + dictionary['title'] + '</title>')
    # icon
    if 'icon' in dictionary:
        if len(dictionary['icon']):
            temp.append('<link rel="shortcut icon" href="' + dictionary['icon'] + '" />')
    # description
    if 'description' in dictionary:
        if len(dictionary['description']):
            temp.append('<meta name="description" content="' + dictionary['description'] + '" />')
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

    '''Preview'''

    # og:site_name
    if 'title' in dictionary:
        if len(dictionary['title']):
            temp.append('<meta property="og:site_name" content="' + dictionary['title'] + '" />')
    # og:title
    if 'title' in dictionary:
        if len(dictionary['title']):
            temp.append('<meta property="og:title" content="' + dictionary['title'] + '" />')
    # og:image (http)
    if 'preview' in dictionary or 'icon' in dictionary:
        if len(dictionary['preview']):
            temp.append('<meta property="og:image" content="' + dictionary['preview'] + '" />')
        elif len(dictionary['icon']):
            temp.append('<meta property="og:image" content="' + dictionary['icon'] + '" />')
    # og:image:secure_url (https)
    if 'preview' in dictionary or 'icon' in dictionary:
        if len(dictionary['preview']):
            temp.append('<meta property="og:image:secure_url" content="' + dictionary['preview'] + '" />')
        elif len(dictionary['icon']):
            temp.append('<meta property="og:image:secure_url" content="' + dictionary['icon'] + '" />')
    # og:description
    if 'description' in dictionary:
        if len(dictionary['description']):
            temp.append('<meta property="og:description" content="' + dictionary['description'] + '" />')
    
    return temp


def add_facebook(dictionary, temp):

    '''Social accounts'''

    # fb:pages
    if 'fb:pages' in dictionary:
        if len(dictionary['fb:pages']):
            pages = ''
            for x in dictionary['fb:pages']:
                pages += x + ', '
            pages = pages[0:-2]
            temp.append('<meta property="fb:pages" content="' + pages + '" />')

    '''Apps'''

    # fb:app_id
    if 'fb:app_id' in dictionary:
        if len(dictionary['fb:app_id']):
            temp.append('<meta porperty="fb:app_id" content="' + dictionary['fb:app_id'] + '" />')

    return temp


def add_twitter(dictionary, temp):

    '''Special'''

    # tw:card
    if 'tw:card' in dictionary:
        if len(dictionary['tw:card']):
            temp.append('<meta name="tw:card" content="' + dictionary['tw:card'] + '">')
    # twitter:domain
    if 'tw:domain' in dictionary:
        if len(dictionary['tw:domain']):
            temp.append('<meta name="twitter:domain" content="' + dictionary['tw:domain'] + '">')

    '''Preview'''

    # twitter:title
    if 'title' in dictionary:
        if len(dictionary['title']):
            temp.append('<meta name="twitter:title" content="' + dictionary['title'] + '" />')
    # twitter:image
    if 'preview' in dictionary or 'icon' in dictionary:
        if len(dictionary['preview']):
            temp.append('<meta name="twitter:image" content="' + dictionary['preview'] + '" />')
        elif len(dictionary['icon']):
            temp.append('<meta name="twitter:image" content="' + dictionary['icon'] + '" />')
    # twitter:description
    if 'description' in dictionary:
        if len(dictionary['description']):
            temp.append('<meta name="twitter:description" content="' + dictionary['description'] + '" />')

    '''Social accounts'''

    # twitter:site
    if 'tw:page' in dictionary:
        if len(dictionary['tw:page']):
            temp.append('<meta name="twitter:site" content="' + dictionary['tw:page'] + '" />')
    # tw:creator
    if 'tw:creator' in dictionary:
        if len(dictionary['tw:creator']):
            temp.append('<meta property="tw:creator" content="' + dictionary['tw:creator'] + '" />')

    '''Apps'''

    # twitter:app:id:googleplay
    if 'tw:googleplay' in dictionary:
        if len(dictionary['tw:googleplay']):
            temp.append('<meta property="twitter:app:id:googleplay" content="' + dictionary['tw:googleplay'] + '" />')
    # twitter:app:id:ipad
    if 'tw:ipad' in dictionary:
        if len(dictionary['tw:ipad']):
            temp.append('<meta property="twitter:app:id:ipad" content="' + dictionary['tw:ipad'] + '" />')
    # twitter:app:id:iphone
    if 'tw:iphone' in dictionary:
        if len(dictionary['tw:iphone']):
            temp.append('<meta property="twitter:app:id:iphone" content="' + dictionary['tw:iphone'] + '" />')

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
        if args.special:
            temp = add_special(dictionary, temp)
        if args.basic:
            temp = add_basic(dictionary, temp)
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
