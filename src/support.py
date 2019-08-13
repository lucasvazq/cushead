#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from ._info import get_info


INFO = get_info()

CURRENT_PYTHON = sys.version_info[:2]
MIN_PYTHON = INFO['python_min_version']
MAX_PYTHON = INFO['python_max_version']

UNSUPPORTED_INSTALLATION = """\
{separators}
Unsupported Python version
{separators}
This version of {name} requires Python >={min_major}.{min_minor} and \
<{max_major}.{max_minor}, but you're trying to
install it with Python {current_major}.{current_minor}
Make sure you have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
    $ python3 -m pip install {name}
This will update pip and setuptools, and install the latest version of
{name}, make sure you still trying to install and running it with a
supported version of python.""".format(**{
    'separators': "="*26,
    'name': INFO['name'],
    'min_major': MIN_PYTHON[0],
    'min_minor': MIN_PYTHON[1],
    'max_major': MAX_PYTHON[0],
    'max_minor': MAX_PYTHON[1],
    'current_major': CURRENT_PYTHON[0],
    'current_minor': CURRENT_PYTHON[1]})

UNSUPPORTED_RUN = """\
{separators}
Unsupported Python version
{separators}
This version of {name} requires Python >={min_major}.{min_minor} and \
<{max_major}.{max_minor}, but you're trying to
run it with Python {current_major}.{current_minor}
Try running:
    $ python3 {name}""".format(**{
    'separators': "="*26,
    'name': INFO['name'],
    'min_major': MIN_PYTHON[0],
    'min_minor': MIN_PYTHON[1],
    'max_major': MAX_PYTHON[0],
    'max_minor': MAX_PYTHON[1],
    'current_major': CURRENT_PYTHON[0],
    'current_minor': CURRENT_PYTHON[1]})


class Support():

    @staticmethod
    def check(message):
        if CURRENT_PYTHON < MIN_PYTHON or CURRENT_PYTHON > MAX_PYTHON:
            sys.stderr.write(message)
            sys.exit(1)

    def install(self):
        self.check(UNSUPPORTED_INSTALLATION)

    def run(self):
        self.check(UNSUPPORTED_RUN)
