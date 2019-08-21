#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import textwrap
from os import path

import argparse

from .helpers import Errors

class Arguments:
    info = None

    def __init__(self, args):
        self.args = self._parse_args(args)
        super().__init__()

    def _parse_args(self, args):
        name = self.info['package_name']
        parser = argparse.ArgumentParser(
            prog=self.info['package_name'],
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage=f"{self.info['package_name']} -file FILEPATH",
            epilog=textwrap.dedent(f"""\
                Examples:
                1) Generate config file:
                    {name} -preset settings.txt
                2) Execute with using that config file:
                    {name} -file settings.txt""")
        )

        # ARGUMENTS

        options = parser.add_argument_group('Options (one required)')

        # -preset
        options.add_argument(
            '-preset',
            metavar='FILENAME',
            dest='preset',
            help=textwrap.dedent("""\
                Name of config file.
                Generate an example config file. That file contains a variable
                named 'config' that can be customized. It has some required
                values: 'html_file' (FILE PATH), 'output' (FOLDER PATH) and
                'static_url' (STRING). Also, if 'icon_png' (IMAGE FILE PATH) is
                declared, this key need to have a value related to a path of an
                existing image.""")
        )
        # -file
        options.add_argument(
            '-file',
            metavar='FILEPATH',
            dest='file',
            help=textwrap.dedent("""\
                Path to the config file.
                Read a config file that contains configurable values related to
                SEO and UX. After it, the script edits an html file and generate
                complementary files like icons, robots.txt, etc.""")
        )

        parser = parser.parse_args(args)

        # Validation
        if not (parser.preset or parser.file):
            Errors.error_message("Miss arguments. Use -preset or -file")
        if parser.preset and parser.file:
            Errors.error_message("Can't use -preset and -file arguments "
                                 "together.")
        if parser.file:
            Errors.exists(parser.file, "-file")
            Errors.is_file(parser.file, "-file")

        return parser
