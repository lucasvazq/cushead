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
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of cushead.py requires Python >=3.5 and <4, but you're trying to
run it with Python {}.{}.
Try running:
    $ python3 cushead.py
""".format(
        *(CURRENT_PYTHON))
    )
    sys.exit(1)

from importlib import machinery
from os import name as os_name
from os import getcwd
from os.path import join
import types

from cushead import main


# Obtain version
def get_version(file):

    name = file
    file = join(getcwd(), file)

    loader = machinery.SourceFileLoader(name, file)
    mod = types.ModuleType(loader.name)
    loader.exec_module(mod)

    return mod.__version__


if os_name == 'nt':
    COLOR = ''
    RESET = ''
else:
    COLOR = '\033[1;34m'
    RESET = '\033[0;0m'
print('''{}
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
                       
Author: Lucas Vazquez
Mail: lucas5zvazquez@gmail.com
Page: https://github.com/lucasvazq
License: MIT
Source: https://github.com/lucasvazq/cushead.py

For help run: python3 cushead.py -h
{}
'''.format(COLOR, get_version('./_version.py'), RESET))


if __name__ == '__main__':
    main(sys.argv[1:])
