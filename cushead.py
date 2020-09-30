#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main script thats run the CLI feature
"""
import importlib
import sys

from src import support


def main():
    support.check_if_can_execute()
    console = importlib.import_module("src.console.console")
    console.parse_args(args=sys.argv[1:])


if __name__ == "__main__":
    main()
