#!/usr/bin/env python
# -*- coding: utf-8 -*-

import textwrap

from .complementary_files import ComplementaryFiles


class Head(ComplementaryFiles):

    def __init__(self, config=None):
        self.config = config
        ComplementaryFiles.__init__(self)
        super().__init__()

    def add_general_config(self):
        # content-type
        head = []
        if 'content-type' in self.config:
            head.append("<meta http-equiv='Content-Type' content='{}' />".format(
                self.config['content-type']))
        # x-ua-compatible
        if 'X-UA-Compatible' in self.config:
            head.append("<meta http-equiv='X-UA-Compatible' content='{}' />".format(
                self.config['X-UA-Compatible']))
        # viewport
        if 'viewport' in self.config:
            concat = (''.join("{}={}, ".format(
                str(content), str(self.config['viewport'][content])) \
                for content in self.config['viewport']))[0:-2]
            head.append("<meta name='viewport' content='{}' />".format(concat))
        # locale
        if 'locale' in self.config:
            head.append("<meta http-equiv='Content-Language' content='{}' />".format(
                self.config['locale']))
        # theme-color and msapplication-TileColor
        if 'color' in self.config:
            head.append("<meta name='theme-color' content='{}' />".format(
                self.config['color']))
            head.append("<meta name='msapplication-TileColor' content='{}' />".format(
                self.config['color']))
        # robots
        if 'robots' in self.config:
            head.append("<meta name='robots' content='{}' />".format(
                self.config['robots']))

        return head

    def add_basic_config(self):
        head = []
        # title
        if 'title' in self.config:
            head.append("<title>{}</title>".format(self.config['title']))
            head.append("<meta name='application-name' content='{}'>".format(
                self.config['title']))
        # description
        if 'description' in self.config:
            head.append("<meta name='description' content='{}' />".format(
                self.config['description']))
        # subject
        if 'subject' in self.config:
            head.append("<meta name='subject' content='{}' />".format(
                self.config['subject']))
        # keywords
        if 'keywords' in self.config:
            head.append("<meta name='keywords' content='{}' />".format(
                self.config['keywords']))

        return head

    def add_social_media(self):
        head = []

        # OPENGRAPH AND FACEBOOK

        # fb:app_id
        if 'fb:app_id' in self.config:
            head.append("<meta porperty='fb:app_id' content='{}' />".format(
                self.config['fb:app_id']))
        # og:locale
        if 'locale' in self.config:
            head.append("<meta property='og:locale' content='{}' />".format(
                self.config['locale']))
        # og:type
        if 'og:type' in self.config:
            head.append("<meta property='og:type' content='{}' />".format(
                self.config['type']))
        # og:url, Likes and Shared are stored under this url
        if 'url' in self.config:
            head.append("<meta property='og:url' content='{}{}' />".format(
                self.config.get('protocol', ''), self.config['url']))
        # og:site_name
        if 'title' in self.config:
            head.append("<meta property='og:site_name' content='{}' />".format(
                self.config['title']))
        # og:title
        if 'title' in self.config:
            head.append("<meta property='og:title' content='{}' />".format(
                self.config['title']))
        # og:description
        if 'description' in self.config:
            head.append("<meta property='og:description' content='{}' />".format(
                self.config['description']))
        # og:image (http) and og:image:secure_url (https)
        if 'preview' in self.config or 'icon' in self.config:
            if 'preview' in self.config:
                head.append("<meta property='og:image' content='{}' />".format(
                    self.config['preview']))
                head.append("<meta property='og:image:secure_url' content='{}' />".format(
                    self.config['preview']))
            else:
                head.append("<meta property='og:image' content='{}' />".format(
                    self.config['icon']))
                head.append("<meta property='og:image:secure_url' content='' />".format(
                    self.config['icon']))
        # og:image:type
        if 'preview_type' in self.config:
            head.append("<meta property='og:image:type' content='{}' />".format(
                self.config['preview_type']))
        # og:image:alt and twitter:image:alt
        if 'title' in self.config or 'description' in self.config:
            title = self.config.get('title', '')
            description = self.config.get('description', '')
            connector = ' - ' if 'title' in self.config and \
                'description' in self.config else ''
            text = "{}{}{}".format(title, connector, description)
            head.append("<meta property='og:image:alt' content='{}' />".format(text))
            head.append("<meta name='twitter:image:alt' content='{}' />".format(text))

        # TWITTER
        # twitter:image:alt mixed with op:image:alt in OPENGRAPH section.

        head.append("<meta name='twitter:card' content='summary' />")
        # twitter:site
        if 'tw:site' in self.config:
            head.append("<meta name='twitter:site' content='{}' />".format(
                self.config['tw:site']))
        # twitter:title
        if 'title' in self.config:
            head.append("<meta name='twitter:title' content='{}' />".format(
                self.config['title']))
        # twitter:description
        if 'description' in self.config:
            head.append("<meta name='twitter:description' content='{}' />".format(
                self.config['description']))
        # twitter:image
        if 'preview' in self.config or 'icon' in self.config:
            if 'preview' in self.config:
                head.append("<meta name='twitter:image' content='{}' />".format(
                    self.config['preview']))
            else:
                head.append("<meta name='twitter:image' content='{}' />".format(
                    self.config['icon']))
        # tw:creator
        if 'tw:creator:id' in self.config:
            head.append("<meta property='twitter:creator:id' content='{}' />".format(
                self.config['tw:creator:id']))

        return head

    def add_author(self):
        head = []
        # author
        if 'author' in self.config:
            head.append("<meta name='author' content='{}' />".format(self.config['author']))

        return head

    def head_general(self):
        # Read contents from file as a single string
        file_handle = open(self.config['html_file'], 'r')
        file_string = file_handle.read()
        file_handle.close()

        # Add lang attribute to <html>
        if 'locale' in self.config:
            if len(self.config['locale']):
                if not '<html>' in file_string:
                    print("Miss <html>, cant add lang attribute")
                else:
                    html = "<html lang=\"{}\">".format(self.config['locale'])
                    file_string = file_string.replace('<html>', html)
                    print(("HTML:\n" +
                        "{}".format(html)))

        # Add custom head elements
        space = file_string.split('$head$')
        if not '$head$' in file_string:
            print("Miss $head$, cant add custom elements")
        else:
            head = []
            head.append(self.add_general_config())
            head.append(self.add_basic_config())
            new_head_elements, new_files = self.generate()
            head.append(new_head_elements)
            head.append(self.add_social_media())
            head.append(self.add_author())
            head = [element for array in head for element in array]
            space = space[0].split('\n')
            space = space[len(space) - 1]
            concat = ("<!-- Custom head elements -->\n" + \
                ''.join("{}{}\n".format(space, element) for element in head)) \
                    [0:-1].replace('\'', '"')
            file_string = file_string.replace('$head$', concat)
            sexy = concat.replace(space, '')
            print(textwrap.dedent("""
                HEAD:"""))
            for element in head:
                print(element)
            print(textwrap.dedent("""
                NEW FILES"""))
            for element in new_files:
                print(element)

        return file_string
