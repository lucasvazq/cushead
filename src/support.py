#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Handle supported situations

Classes:
    Messages
"""

# Keep old style format


import os
import sys


(DEFAULT_COLOR, ERROR_COLOR, PRESENTATION_COLOR) = (
    ("", "", "")
    if os.name == "nt"
    else (
        "\033[0;0m",  # DEFAULT
        "\033[1;31m",  # ERROR: Red
        "\033[1;34m",  # PRESENTATION: Blue
    )
)


class Messages:
    """Generate unsupported messages

    Methods:
        unsupported_installation
        unsupported_run
    """

    support_string_format = {}

    def _unsupported_title(self):
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
        title = title.format(title_frame=title_frame, **self.support_string_format)
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
    """Handle situations

    Methods:
        install
        run
    """

    def __init__(self, info):
        self.current_python = sys.version_info[:2]
        self.min_python = info["python_min_version"]
        self.max_python = info["python_max_version"]
        self.support_string_format = {
            "name": info["package_name"],
            "min_major": self.min_python[0],
            "min_minor": self.min_python[1],
            "max_major": self.max_python[0],
            "max_minor": self.max_python[1],
            "current_major": self.current_python[0],
            "current_minor": self.current_python[1],
        }

    def _check(self, message):
        """Check if current version is supported"""
        if (
            self.current_python < self.min_python
            or self.current_python > self.max_python
        ):
            title = self._unsupported_title()
            exception = ERROR_COLOR + title + message + DEFAULT_COLOR
            raise Unsupported(exception)

    def install(self):
        """Check installation support"""
        message = self.unsupported_installation()
        self._check(message)

    def run(self):
        """Check script run support"""
        message = self.unsupported_run()
        self._check(message)


class Unsupported(Exception):
    """Used to raise an exception related to an unsupported versions problem"""

    pass
