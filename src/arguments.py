#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import getcwd, path
from textwrap import dedent

import argparse

from _info import get_info


INFO = get_info()


class Arguments():

    def __init__(self, args):
        self.args = self.parse_args(args)
        super().__init__()

    @staticmethod
    def parse_args(args):
        parser = argparse.ArgumentParser(
            prog=INFO['name'],
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage="{} -file FILEPATH".format(INFO['name']),
            epilog=dedent("""\
                Examples:
                1) Generate config file:
                    {0} -preset custom.txt
                2) Execute with using that config file:
                    {0} -file custom.txt""").format(INFO['name']))

        parser._action_groups.pop()
        options = parser.add_argument_group('Options (one required)')
        options.add_argument('-preset', metavar=('FILENAME'), dest='preset',
            help=dedent("""\
                Name of config file.
                Generate an example config file. That file contains a variable named 'config'
                that can be customized. It has some required values: 'html_file' (FILE PATH),
                'output' (FOLDER PATH) and 'static_url' (STRING). Also, if 'icon_png'
                (IMAGE FILE PATH) is declared, this key need to have a value related to a path
                of an existing image."""))
        options.add_argument('-file', metavar=('FILEPATH'), dest='file',
            help=dedent("""\
                Path to config file.
                Read a config file that contains configurable values related to SEO and UX.
                After it, the script edits an html file and generate complementary files like
                icons, robots.txt, etc."""))

        parser = parser.parse_args(args)
        if not (parser.preset or parser.file):
            # test: test_no_arguments
            raise Exception("Miss arguments. Use -preset or -file")
        if parser.preset and parser.file:
            # test: test_two_arguments
            raise Exception("Can't use -preset and -file arguments together.")
        if parser.file:
            if not path.exists(parser.file):
                # test: test_file_doesnt_exists
                raise Exception(dedent("""\
                    -file ({}) must be referred to a file path that exists.
                    FILE PATH: {}""".format(parser.file,
                        path.join(getcwd(), parser.file))))
            if not path.isfile(parser.file):
                # test: test_file_no_file
                raise Exception(dedent("""\
                    -file ({}) must be referred to a file path.
                    FILE PATH: {}""".format(parser.file,
                        path.join(getcwd(), parser.file))))
        return parser
