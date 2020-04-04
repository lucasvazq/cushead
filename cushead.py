#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main script"""
import importlib
import sys

import src_2.info
import src_2.support


# Check python version
try:
    _INFO = src_2.info.get_info()
    src_2.support.Support(_INFO).check_for_execution()
except src_2.support.Unsupported as exception:
    sys.stdout.write(str(exception))
    sys.exit()
else:
    console = importlib.import_module('src_2.console.console')


def main():
    console.Console(sys.argv[1:]).run()


if __name__ == "__main__":
    main()
