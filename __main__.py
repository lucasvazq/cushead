#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# Check Python version compatibility
CURRENT_PYTHON = sys.version_info[:2]
MIN_PYTHON = (3, 5)
MAX_PYTHON = (4, 0)
if CURRENT_PYTHON < MIN_PYTHON or CURRENT_PYTHON > MAX_PYTHON:
    err = True
else:
    err = False
if err:
    sys.stderr.write(textwrap.dedent("""\
        ==========================
        Unsupported Python version
        ==========================
        This version of cushead.py requires Python >={}.{} and <{},
        but you're trying to run it with Python {}.{}.
        Try running:
            $ python3 cushead.py""".format(*(MIN_PYTHON + MAX_PYTHON +
            CURRENT_PYTHON))))
    sys.exit(1)

from os import name as os_name

from src.main import Main
from _info import get_info


INFO = get_info()


# Blue
(COLOR, RESET) = ('', '') if os_name == 'nt' else ('\033[1;34m', '\033[0;0m')
print("""{}
   ____  _   _  ____   _   _  _____     _     ____     ____ __   __
  / ___|| | | |/ ___| | | | || ____|   / \   |  _ \   |  _ \\\ \ / /
 | |    | | | |\___ \ | |_| ||  _|    / _ \  | | | |  | |_) |\ V / 
 | |___ | |_| | ___) ||  _  || |___  / ___ \ | |_| |_ |  __/  | |  
  \____| \___/ |____/ |_| |_||_____|/_/   \_\|____/(_)|_|     |_|  
                             _       _
                             _/     /
                            /    __/
         UX / SEO         _/  __/           v {}
                         / __/
                        / /
                       /'
                       
Author: {}
Email: {}
Page: {}
License: {}

Git: {}
Documentation: {}

For help run: {} -h
{}""".format(COLOR, INFO['version'], INFO['author'], INFO['email'],
    INFO['author_page'], INFO['license'], INFO['source'], INFO['documentation'],
    INFO['name'], RESET))


if __name__ == '__main__':
    Main(sys.argv[1:]).run()
