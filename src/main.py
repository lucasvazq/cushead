#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import textwrap
from os import path

from .arguments import Arguments
from .config import Config
from .head import Head
from .helpers import Helpers
from .presets import Presets


class Main(Arguments, Presets, Config, Head, Helpers):

    def __init__(self, info, args):
        self.info = info
        super().__init__(args)

    def run(self):

        # -presets
        if self.args.preset:
            self.make_preset(self.args.preset)
            filepath = path.join(os.getcwd(), self.args.preset)
            print(
                f"PATH: {self.args.preset}\n"
                f"FULL PATH: {filepath}"
            )

        # -file
        else:
            config = self.get_values()
            output_filepath = path.join(os.getcwd(),
                                        self.config['files_output'])
            html_filepath = path.join(output_filepath, 'index.html')
            head = self.head_general()
            self.write_file(html_filepath, head)
            print(
                f"OUTPUT FILES: {config['files_output']}\n"
                f"(full path): {output_filepath}"
            )
