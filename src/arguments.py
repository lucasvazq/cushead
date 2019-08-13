#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import textwrap

import argparse

from _info import get_info


INFO = get_info()


class Arguments():

    def __init__(self, args=None):
        self.args = self.parse_args(args)
        super().__init__()

    def parse_args(self, args):
        parser = argparse.ArgumentParser(
            prog=INFO['name'],
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage="{} -file FILEPATH".format(INFO['name']),
            epilog=textwrap.dedent("""\
                Examples:
                1) Generate config file:
                    {0} -preset custom.txt
                2) Execute with using that config file:
                    {0} -file custom.txt""").format(INFO['name']))

        parser._action_groups.pop()
        options = parser.add_argument_group('Options (one required)')
        options.add_argument('-file', metavar=('FILEPATH'), dest='file',
            help=textwrap.dedent("""\
                Path to config file.
                Read a config file that contains configurable values related to SEO and UX.
                After it, the script edits an html file and generate complementary files like
                icons, robots.txt, etc."""))
        options.add_argument('-preset', metavar=('FILENAME'), dest='preset',
            help=textwrap.dedent("""\
                Name of config file.
                Generate an example config file. That file contain some required values like
                'html_file' (FILE), 'output' (FOLDER) and 'static_url' (STRING). Also, if
                'icon_png' (IMAGE FILEPATH) is declared, this key need to have value related
                to a path of an existing image."""))

        parser = parser.parse_args(args)
        if not (parser.preset or parser.file):
            raise Exception(textwrap.dedent("""\
                Miss -file argument. Do '{} -h' for help.""".format(INFO['name'])))
        if parser.preset and parser.file:
            raise Exception(textwrap.dedent("""\
                Can't use -preset and -file arguments together. Do '{} -h' for help."""
                    .format(INFO['name'])))
        if parser.file:
            if not path.isfile(parser.file):
                raise Exception("File passed by -file ({}) can't be found.".format(
                    str(parser.file)))

        return parser
