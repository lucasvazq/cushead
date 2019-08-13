#!/usr/bin/env python
# -*- coding: utf-8 -*-

from importlib import machinery
from os import getcwd
from os.path import join
import types


class Helpers():

    @staticmethod
    def _get_values(filename):
        filepath = join(getcwd(), filename)
        loader = machinery.SourceFileLoader(filename, filepath)
        mod = types.ModuleType(loader.name)
        loader.exec_module(mod)
        return mod.values

    @staticmethod
    def _write_file(filepath, content):
        file_handle = open(filepath, 'w')
        file_handle.write(content)
        file_handle.close()
        return filepath
