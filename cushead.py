#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import textwrap

from src.info import Info
from src.support import Support

# Check python version
try:
    INFO = Info().get_info()
    Support(INFO).run()
except Exception as e:
    print(e)
    sys.exit()

from src.main import Main


# Blue
(COLOR, RESET) = (
    ('', '')
    if os.name == 'nt' else
    (
        '\033[1;34m',  # Blue
        '\033[0;0m'  # Default
    )
)

# Console output in ./doc/presentation.png
message = textwrap.dedent(f"""{COLOR}\
       ____  _   _  ____   _   _  _____     _     ____     ____ __   __
      / ___|| | | |/ ___| | | | || ____|   / \\   |  _ \\   |  _ \\\\ \\ / /
     | |    | | | |\\___ \\ | |_| ||  _|    / _ \\  | | | |  | |_) |\\ V / 
     | |___ | |_| | ___) ||  _  || |___  / ___ \\ | |_| |_ |  __/  | |  
      \\____| \\___/ |____/ |_| |_||_____|/_/   \\_\\|____/(_)|_|     |_|  
                                 __       _
                                 _/     /
                                /    __/
             UX / SEO         _/  __/           v {INFO['package_version']}
                             / __/
                            / /
                           /'
    
    Author: {INFO['author']}
    Email: {INFO['email']}
    Page: {INFO['author_page']}
    License: {INFO['license']}
    
    Git: {INFO['source']}
    Documentation: {INFO['documentation']}
    For help run: {INFO['package_name']} -h
    {RESET}""")


def main():
    print(message)
    Main(INFO, sys.argv[1:]).run()


if __name__ == '__main__':
    main()
