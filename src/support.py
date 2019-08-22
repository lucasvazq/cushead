#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Handle supported situations"""

import sys

from .console import DEFAULT_COLOR, ERROR_COLOR


class Unsupported(Exception):
    """Used to raise an exception related to an unsupported versions problem"""


class Messages:
    """Generate unsupported messages"""
    support_string_format = {}

    def unsupported_title(self):
        """Generate unsupported title presentation"""
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
        """Generate unsupported message for the installation attempt"""
        string = (
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
        string = string.format(**self.support_string_format)
        return string

    def unsupported_run(self):
        """Generate unsupported message for the run script attempt"""
        string = (
            "but you're trying to run it with Python "
            "{current_major}.{current_minor}\n"
            "Try running:\n"
            "   $ python3 ./{name}.py\n"
        )
        string = string.format(**self.support_string_format)
        return string


class Support(Messages):
    """Handle situations"""

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
        """Check if current version is supported"""
        if self.current_python < self.min_python or \
                self.current_python > self.max_python:
            title = self.unsupported_title()
            exception = (
                ERROR_COLOR
                + title
                + message
                + DEFAULT_COLOR
            )
            raise Unsupported(exception)

    def install(self):
        """Check installation support"""
        message = self.unsupported_installation()
        self.check(message)

    def run(self):
        """Check script run support"""
        message = self.unsupported_run()
        self.check(message)
