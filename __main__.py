#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _info import get_info
from src.support import Support
INFO = get_info()
Support(INFO).install()

import sys
from os import name as os_name

from src.main import Main


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
    Main(INFO, sys.argv[1:]).run()
