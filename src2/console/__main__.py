#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Arguments handler"""

import os
from os import path

from src2.console.arguments import parse_args
from src2.console.config import get_values
from src2.module.files import Files
from src2.helpers import FilesHelper, FoldersHelper
from src2.main import Main as ModuleMain
from src2.module.presets import Presets
from ..info import get_info


class Main(ModuleMain):
    """Main class of this module"""

    def __init__(self, args):
        self.info = get_info()
        self.args = parse_args(args, self.info)
        self.config = get_values(self.args) if self.args.file else {}
        super().__init__()

    def run(self):
        """Handle the different arguments"""

        # -presets
        if self.args.preset:
            default_settings = self.default_settings()
            FilesHelper.write_file(self.args.preset, default_settings)
            if self.args.images:
                binary_images = self.default_images()
                realpath = path.join(path.dirname(path.realpath(__file__)), 'assets')
                destination_folder = ''.join(self.args.preset.split('/')[0:-1])
                for binary_image in binary_images:
                    filepath = path.join(realpath, filename)
                    destination = path.join(destination_folder, filename)
                    FilesHelper.wirte_binary(filepath, destination)
            fullpath = path.join(os.getcwd(), self.args.preset)
            print(
                f"CONFIG FILE: {self.args.preset}\n"
                f"(full path): {fullpath}"
            )
            return '-preset'
        else:
            print('-file')