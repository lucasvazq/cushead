#!/usr/bin/env python
# -*- coding: utf-8 -*-

from importlib import machinery
from os import getcwd, path
import textwrap

from .arguments import Arguments
from .head import Head
from .helpers import Helpers
from .presets import Presets


class Main(Arguments, Presets, Head, Helpers):

    def __init__(self, args):
        super().__init__(args)

    def run(self):

        # -presets
        if self.args.preset:
            self._make_preset(self.args.preset)
            print(textwrap.dedent("""
                PATH: {}
                FULLPATH: {}""".format(self.args.preset, path.join(getcwd(),
                    self.args.preset))))
        # -file
        else:
            self.values = self._get_values(self.args.file)
            if not 'html_file' in self.values:
                raise Exception("Miss 'html_file' key in {} and its required.".format(
                    self.args.file))
            if not len(self.values['html_file']):
                raise Exception("'html_file' key value can't be void.")
            if not 'output' in self.values:
                raise Exception("Miss 'output' key in {} and it's required.".format(
                    self.args.file))
            if not path.exists(self.values['output']):
                raise Exception("'output' key must be referred to a directory that exists.")
            if not path.isdir(self.values['output']):
                raise Exception("'output' key must be referred to a directory.")
            if not 'static_url' in self.values:
                raise Exception("Miss 'static_url' key in {} and it's required.".format(
                    self.args.file))

            # write html file
            self._write_file(self.values['html_file'], self.head_general())

            print(textwrap.dedent("""
                HTML FILE: {}
                (full path): {}
                OUTPUT FILES: {}
                (full path): {}""".format(self.values['html_file'], path.join(getcwd(),
                    self.values['html_file']), self.values['output'], path.join(getcwd(),
                    self.values['output']))))
