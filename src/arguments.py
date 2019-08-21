#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import textwrap
from os import path

import argparse


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

        # Parse arguments
        parser = parser.parse_args(args)

        # Test: test_no_arguments
        # Action: get in
        if not (parser.preset or parser.file):
            raise Exception("Miss arguments. Use -preset or -file")

        # Test: test_two_arguments
        # Action: get in
        if parser.preset and parser.file:
            raise Exception("Can't use -preset and -file arguments together.")

        if parser.file:
            file = parser.file
            filepath = path.join(os.getcwd(), file)

            # Test: test_file_doesnt_exists
            # Action: get in
            if not path.exists(filepath):
                e = (
                    f"-file ({file}) must be referred to a file path that "
                    "exists.\n"
                    f"FILE PATH: {filepath}"
                )
                raise Exception(e)

            # Test: test_file_no_file
            # Action: get in
            if not path.isfile(parser.file):
                e = textwrap.dedent(f"""\
                    -file ({file}) must be referred to a file path.
                    FILE PATH: {filepath}""")
                raise Exception(e)

        return parser
