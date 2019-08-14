#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import textwrap
from os import path

from .arguments import Arguments
from .head import Head
from .helpers import Helpers
from .presets import Presets

def main():
    print("WASAAA")

class Main(Arguments, Presets, Head, Helpers):

    def __init__(self, info, args):
        self.info = info
        super().__init__(args)

    def run(self):

        # -presets
        if self.args.preset:
            self._make_preset(self.args.preset)
            print(textwrap.dedent("""
                PATH: {}
                FULL PATH: {}""".format(self.args.preset, path.join(os.getcwd(),
                    self.args.preset))))
        # -file
        else:
            self.config = self._get_values(self.args.file)
            if not 'html_file' in self.config:
                # test: test_miss_html_file
                raise Exception("Miss 'html_file' key and it's required.")
            if not len(self.config['html_file']):
                # test: test_void_html_file
                raise Exception("'html_file' value can't be void.")
            if not path.exists(self.config['html_file']):
                # test: test_html_file_doesnt_exists
                raise Exception(textwrap.dedent("""\
                    'html_file' ({}) must be referred to a file path that exists.
                    FILE PATH: {}""".format(self.config['html_file'],
                        path.join(os.getcwd(), self.config['html_file']))))
            if not path.isfile(self.config['html_file']):
                # test: test_html_file_no_file
                raise Exception(textwrap.dedent("""\
                    'html_file' ({}) must be referred to a file path.
                    FILE PATH: {}""".format(self.config['html_file'],
                        path.join(os.getcwd(), self.config['html_file']))))
            if not 'output' in self.config:
                # test: test_miss_output
                raise Exception("Miss 'output' key and it's required.")
            if not path.exists(self.config['output']):
                # test: test_output_doesnt_exists
                raise Exception(textwrap.dedent("""\
                    'output' ({}) must be referred to a folder path that exists.
                    FOLDER PATH: {}""".format(self.config['output'],
                        path.join(os.getcwd(), self.config['output']))))
            if not path.isdir(self.config['output']):
                # test: test_output_no_folder
                raise Exception(textwrap.dedent("""\
                    'output' ({}) must be referred to a folder path.
                    FOLDER PATH: {}""".format(self.config['output'],
                        path.join(os.getcwd(), self.config['output']))))
            if not 'static_url' in self.config:
                # test: test_miss_static_url
                raise Exception("Miss 'static_url' key and it's required.")

            # Write html file
            self._write_file(self.config['html_file'], self.head_general())

            print(textwrap.dedent("""
                HTML FILE: {}
                (full path): {}
                OUTPUT FILES: {}
                (full path): {}""".format(self.config['html_file'], path.join(os.getcwd(),
                    self.config['html_file']), self.config['output'], path.join(os.getcwd(),
                    self.config['output']))))
