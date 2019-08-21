#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main script of cushead, a python CLI"""

import sys

from src.support import Unsupported

# Check python version
try:
    from src.info import Info
    from src.support import Support
    INFO = Info().get_info()
    Support(INFO).run()
except Unsupported as exception:
    sys.stdout.write(exception)
    sys.exit()

from src.console import PRESENTATION_MESSAGE
from src.main import Main


def main():

    """Main function"""

    print(PRESENTATION_MESSAGE)
    Main(INFO, sys.argv[1:]).run()


if __name__ == '__main__':
    main()
