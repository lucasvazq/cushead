#!/home/lucas/Lucas/Projects/wasa/venv_test/bin/python
# -*- coding: utf-8 -*-

from src.info import Info
from src.support import Support
INFO = Info().get_info()
Support(INFO).run()

import os
import sys

from src.main import Main


# Blue
(COLOR, RESET) = ('', '') if os.name == 'nt' else ('\033[1;34m', '\033[0;0m')
message = ("""{}
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
{}""".format(COLOR, INFO['package_version'], INFO['author'], INFO['email'],
    INFO['author_page'], INFO['license'], INFO['source'], INFO['documentation'],
    INFO['package_name'], RESET))


def main():
    print(message)
    Main(INFO, sys.argv[1:]).run()


if __name__ == '__main__':
    main()
