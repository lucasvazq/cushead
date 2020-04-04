#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Disable modules import order on Pylint because it generate a warning
# Need to call some functions before call rest of methods for check the python
# version and generate a custom alert message to the user.
# pylint: disable=C0413
"""Main script"""
import sys

import src_2.info
import src_2.support


# Check python version
try:
    INFO = src_2.info.Info.get_info()
    src_2.support.Support(INFO).check_for_execution()
except src_2.support.Unsupported as exception:
    sys.stdout.write(str(exception))
    sys.exit()
else:
    import src_2.console.console


def main():
    src_2.console.console.Console(sys.argv[1:]).run()


if __name__ == "__main__":
    main()
