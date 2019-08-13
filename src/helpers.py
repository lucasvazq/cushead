#!/usr/bin/env python
# -*- coding: utf-8 -*-

import types
from importlib import machinery
from os import getcwd, path
from textwrap import dedent


class Helpers():

    def __init__(self, args=None):
        self.args = args

    def _get_values(self, filename):
        filepath = path.join(getcwd(), filename)
        loader = machinery.SourceFileLoader(filename, filepath)
        mod = types.ModuleType(loader.name)
        loader.exec_module(mod)
        try:
            return mod.config
        except:
            raise Exception(dedent("""\
                Can't found 'config' variable in ({})
                FILE PATH: {}""".format(self.args.file,
                    path.join(getcwd(), self.args.file))))

    @staticmethod
    def _write_file(filepath, content):
        file_handle = open(filepath, 'w')
        file_handle.write(content)
        file_handle.close()
        return filepath
