#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from cushead import main

CURRENT_PYTHON = sys.version_info[:2]
MIN_PYTHON = (3, 5)
MAX_PYTHON = (4, 0)
if CURRENT_PYTHON < MIN_PYTHON or CURRENT_PYTHON > MAX_PYTHON:
    err = True
else:
    err = False
if err:
    raise Exception("Python >=3.5 and <4 is required.")

if __name__ == '__main__':
    main(sys.argv[1:])
