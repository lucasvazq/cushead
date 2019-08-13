#!/usr/bin/env python
# -*- coding: utf-8 -*-

import types
from importlib import machinery
from textwrap import dedent
from os import getcwd, path


class Helpers():

    @staticmethod
    def _get_values(filename):
        filepath = path.join(getcwd(), filename)
        loader = machinery.SourceFileLoader(filename, filepath)
        mod = types.ModuleType(loader.name)
        loader.exec_module(mod)
        if not 'config' in mod:
            raise Exception(dedent("""\
                Can't found 'config' variable in ({})
                FILE PATH: {}""".format(self.args.file,
                    path.join(getcwd(), self.args.file))))
        return mod.config

    @staticmethod
    def _write_file(filepath, content):
        file_handle = open(filepath, 'w')
        file_handle.write(content)
        file_handle.close()
        return filepath
