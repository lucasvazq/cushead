#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from .console import DEFAULT_COLOR, ERROR_COLOR


class Messages:
    support_string_format = None

    def unsupported_title(self):
        title = "Unsupported Python version"
        title_length = len(title)
        title_frame = "=" * title_length
        title = (
            "{title_frame}\n"
            "Unsupported Python version\n"
            "{title_frame}\n"
            "This version of {name} requires Python >={min_major}.{min_minor} "
            "and <{max_major}.{max_minor},\n"
        )
        title = title.format(title_frame=title_frame,
                             **self.support_string_format)
        return title

    def unsupported_installation(self):
        s = (
            "but you're trying to install it with Python "
            "{current_major}.{current_minor}\n"
            "Make sure you have pip and setuptools updated, then try again.\n"
            "   $ python3 -m pip install --upgrade pip setuptools\n"
            "   $ python3 -m pip install {name}\n"
            "This will update pip and setuptools, and install the latest "
            "version \n"
            "of {name}, make sure you still running it with a supported "
            "version \n"
            "of Python.\n"
        )
        s = s.format(**self.support_string_format)
        return s

    def unsupported_run(self):
        s = (
            "but you're trying to run it with Python "
            "{current_major}.{current_minor}\n"
            "Try running:\n"
            "   $ python3 ./{name}.py\n"
        )
        s = s.format(**self.support_string_format)
        return s


class Support(Messages):

    def __init__(self, info):
        self.current_python = sys.version_info[:2]
        self.min_python = info['python_min_version']
        self.max_python = info['python_max_version']
        self.support_string_format = {
            'name': info['package_name'],
            'min_major': self.min_python[0],
            'min_minor': self.min_python[1],
            'max_major': self.max_python[0],
            'max_minor': self.max_python[1],
            'current_major': self.current_python[0],
            'current_minor': self.current_python[1],
        }

    def check(self, message):
        if (
            self.current_python < self.min_python or
            self.current_python > self.max_python
        ):
            title = self.unsupported_title()
            sys.stdout.write(
                ERROR_COLOR
                + title
                + message
                + DEFAULT_COLOR
            )
            sys.exit()

    def install(self):
        message = self.unsupported_installation()
        self.check(message)

    def run(self):
        message = self.unsupported_run()
        self.check(message)
