#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


def unsupported_title():
    title = "Unsupported Python version"
    return """\
{0}
{1}
{0}
""".format("="*len(title), title)


def unsupported_installation(info, support_string_format):
    return """\
This version of {name} requires Python >={min_major}.{min_minor} and \
<{max_major}.{max_minor}, but you're trying to
install it with Python {current_major}.{current_minor}
Make sure you have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
    $ python3 -m pip install {name}
This will update pip and setuptools, and install the latest version of
{name}, make sure you still trying to install and running it with a
supported version of python.
""".format(**support_string_format)


def unsupported_run(info, support_string_format):
    return """\
This version of {name} requires Python >={min_major}.{min_minor} and \
<{max_major}.{max_minor}, but you're trying to
run it with Python {current_major}.{current_minor}
Try running:
    $ python3 {name}
""".format(**support_string_format)


class Support():

    def __init__(self, info):
        self.info = info
        self.current_python = sys.version_info[:2]
        self.min_python = self.info['python_min_version']
        self.max_python = self.info['python_max_version']
        self.support_string_format = {
            'name': self.info['package_name'],
            'min_major': self.min_python[0],
            'min_minor': self.min_python[1],
            'max_major': self.max_python[0],
            'max_minor': self.max_python[1],
            'current_major': self.current_python[0],
            'current_minor': self.current_python[1]}

    def check(self, message):
        if self.current_python < self.min_python or \
            self.current_python > self.max_python:
            sys.stderr.write(unsupported_title() + message)
            sys.exit(1)

    def install(self):
        self.check(unsupported_installation(self.info, self.support_string_format))

    def run(self):
        self.check(unsupported_run(self.info, self.support_string_format))
