#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Disable modules import order on Pylint because it generate a warning
# Need to call some functions before call rest of methods for check the python
# version and generate a custom alert message to the user.
# pylint: disable=C0413

"""Main script"""

import sys

from src.info import get_info
from src.support import Support, Unsupported

# Check python version
try:
    INFO = get_info()
    Support(INFO).run()
except Unsupported as exception:
    sys.stdout.write(exception)
    sys.exit()

from src.console.__main__ import Main


def main():
    """Main function"""
    Main(sys.argv[1:]).run()


if __name__ == '__main__':
    main()
