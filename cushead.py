#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# Check python version
try:
    from src.info import Info
    from src.support import Support
    INFO = Info().get_info()
    Support(INFO).run()
except Exception as e:
    sys.stdout(e)
    sys.exit()

from src.console import PRESENTATION_MESSAGE
from src.main import Main


def main():
    print(PRESENTATION_MESSAGE)
    Main(INFO, sys.argv[1:]).run()


if __name__ == '__main__':
    main()
