#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main script"""
import importlib
import sys

import src.info
import src.support

# Check python version
try:
    _INFO = src.info.get_info()
    src.support.Support(_INFO).check_for_execution()
except src.support.Unsupported as exception:
    sys.stdout.write(str(exception))
    sys.exit()
else:
    console = importlib.import_module("src.console.console")


def main():
    console.Console(sys.argv[1:]).run()


if __name__ == "__main__":
    main()
