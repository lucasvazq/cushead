#!/usr/bin/env python
# -*- coding: utf-8 -*-

import textwrap

from .complementary_files import ComplementaryFiles


class Head(ComplementaryFiles):

    def __init__(self, dictionary=None):
        self.values = dictionary
        ComplementaryFiles.__init__(self)
        super().__init__()

    def add_general_config(self):
        # content-type
        head = []
        if 'content-type' in self.values:
            head.append("<meta http-equiv='Content-Type' content='{}' />".format(
                self.values['content-type']))
        # x-ua-compatible
        if 'X-UA-Compatible' in self.values:
            head.append("<meta http-equiv='X-UA-Compatible' content='{}' />".format(
                self.values['X-UA-Compatible']))
        # viewport
        if 'viewport' in self.values:
            concat = (''.join("{}={}, ".format(
                str(content), str(self.values['viewport'][content])) \
                for content in self.values['viewport']))[0:-2]
            head.append("<meta name='viewport' content='{}' />".format(concat))
        # locale
        if 'locale' in self.values:
            head.append("<meta http-equiv='Content-Language' content='{}' />".format(
                self.values['locale']))
        # theme-color and msapplication-TileColor
        if 'color' in self.values:
            head.append("<meta name='theme-color' content='{}' />".format(
                self.values['color']))
            head.append("<meta name='msapplication-TileColor' content='{}' />".format(
                self.values['color']))
        # robots
        if 'robots' in self.values:
            head.append("<meta name='robots' content='{}' />".format(
                self.values['robots']))

        return head

    def add_basic_config(self):
        head = []
        # title
        if 'title' in self.values:
            head.append("<title>{}</title>".format(self.values['title']))
            head.append("<meta name='application-name' content='{}'>".format(
                self.values['title']))
        # description
        if 'description' in self.values:
            head.append("<meta name='description' content='{}' />".format(
                self.values['description']))
        # subject
        if 'subject' in self.values:
            head.append("<meta name='subject' content='{}' />".format(
                self.values['subject']))
        # keywords
        if 'keywords' in self.values:
            head.append("<meta name='keywords' content='{}' />".format(
                self.values['keywords']))

        return head

    def add_social_media(self):
        head = []

        # OPENGRAPH AND FACEBOOK

        # fb:app_id
        if 'fb:app_id' in self.values:
            head.append("<meta porperty='fb:app_id' content='{}' />".format(
                self.values['fb:app_id']))
        # og:locale
        if 'locale' in self.values:
            head.append("<meta property='og:locale' content='{}' />".format(
                self.values['locale']))
        # og:type
        if 'og:type' in self.values:
            head.append("<meta property='og:type' content='{}' />".format(
                self.values['type']))
        # og:url, Likes and Shared are stored under this url
        if 'url' in self.values:
            head.append("<meta property='og:url' content='{}{}' />".format(
                self.values.get('protocol', ''), self.values['url']))
        # og:site_name
        if 'title' in self.values:
            head.append("<meta property='og:site_name' content='{}' />".format(
                self.values['title']))
        # og:title
        if 'title' in self.values:
            head.append("<meta property='og:title' content='{}' />".format(
                self.values['title']))
        # og:description
        if 'description' in self.values:
            head.append("<meta property='og:description' content='{}' />".format(
                self.values['description']))
        # og:image (http) and og:image:secure_url (https)
        if 'preview' in self.values or 'icon' in self.values:
            if 'preview' in self.values:
                head.append("<meta property='og:image' content='{}' />".format(
                    self.values['preview']))
                head.append("<meta property='og:image:secure_url' content='{}' />".format(
                    self.values['preview']))
            else:
                head.append("<meta property='og:image' content='{}' />".format(
                    self.values['icon']))
                head.append("<meta property='og:image:secure_url' content='' />".format(
                    self.values['icon']))
        # og:image:type
        if 'preview_type' in self.values:
            head.append("<meta property='og:image:type' content='{}' />".format(
                self.values['preview_type']))
        # og:image:alt and twitter:image:alt
        if 'title' in self.values or 'description' in self.values:
            title = self.values.get('title', '')
            description = self.values.get('description', '')
            connector = ' - ' if 'title' in self.values and \
                'description' in self.values else ''
            text = "{}{}{}".format(title, connector, description)
            head.append("<meta property='og:image:alt' content='{}' />".format(text))
            head.append("<meta name='twitter:image:alt' content='{}' />".format(text))

        # TWITTER
        # twitter:image:alt mixed with op:image:alt in OPENGRAPH section.

        head.append("<meta name='twitter:card' content='summary' />")
        # twitter:site
        if 'tw:site' in self.values:
            head.append("<meta name='twitter:site' content='{}' />".format(
                self.values['tw:site']))
        # twitter:title
        if 'title' in self.values:
            head.append("<meta name='twitter:title' content='{}' />".format(
                self.values['title']))
        # twitter:description
        if 'description' in self.values:
            head.append("<meta name='twitter:description' content='{}' />".format(
                self.values['description']))
        # twitter:image
        if 'preview' in self.values or 'icon' in self.values:
            if 'preview' in self.values:
                head.append("<meta name='twitter:image' content='{}' />".format(
                    self.values['preview']))
            else:
                head.append("<meta name='twitter:image' content='{}' />".format(
                    self.values['icon']))
        # tw:creator
        if 'tw:creator:id' in self.values:
            head.append("<meta property='twitter:creator:id' content='{}' />".format(
                self.values['tw:creator:id']))

        return head

    def add_author(self):
        head = []
        # author
        if 'author' in self.values:
            head.append("<meta name='author' content='{}' />".format(self.values['author']))

        return head

    def head_general(self):
        # Read contents from file as a single string
        file_handle = open(self.values['html_file'], 'r')
        file_string = file_handle.read()
        file_handle.close()

        # Add lang attribute to <html>
        if 'locale' in self.values:
            if len(self.values['locale']):
                if not '<html>' in file_string:
                    print("Miss <html>, cant add lang attribute")
                else:
                    html = "<html lang=\"{}\">".format(self.values['locale'])
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
