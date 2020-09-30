#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc
"""
# IMPORTANT: This module would be python2 and python3 compatible

import os
import sys
from collections import namedtuple

from src import info


if os.name == "nt":
    DEFAULT_COLOR = ""
    ERROR_COLOR = ""
    PRESENTATION_COLOR = ""
else:
    DEFAULT_COLOR = "\033[0;0m"
    ERROR_COLOR = "\033[1;31m"
    PRESENTATION_COLOR = "\033[1;34m"


_CURRENT_VERSION = sys.version_info[:2]


def get_unsupported_title(action):
    """
    doc
    """
    support_info = namedtuple(
        typename='SupportString',
        field_names=(
            'min_major',
            'min_minor',
            'current_major',
            'current_minor',
        )
    )(
        min_major=info.PYTHON_MIN_VERSION[0],
        min_minor=info.PYTHON_MIN_VERSION[1],
        current_major=_CURRENT_VERSION[0],
        current_minor=_CURRENT_VERSION[1],
    )
    title = "Unsupported Python version"
    title_length = len(title)
    title_frame = "=" * title_length
    return "\n".join((
        title_frame,
        title,
        title_frame,
        (
            "This version of {package_name} requires Python >={min_major}.{min_minor}, "
            "but you're trying to {action} it with Python {current_major}.{current_minor}"
        ),
    )).format(
        package_name=info.PACKAGE_NAME,
        min_major=support_info.min_major,
        min_minor=support_info.min_minor,
        current_major=support_info.current_major,
        current_minor=support_info.current_minor,
        action=action,
    )


def get_unsupported_installation_message():
    """Generate unsupported message for the installation attempt"""
    return "\n".join((
        get_unsupported_title(action="install"),
        "Make sure you have pip and setuptools updated, then try again.",
        "    $ python3 -m pip install --upgrade pip setuptools",
        "    $ python3 -m pip install {package_name}",
        (
            "This will update pip and setuptools, and install the latest version of {package_name},"
            "make sure you still running it with a supported version of Python"
        ),
    )).format(package_name=info.PACKAGE_NAME)


def get_unsupported_execution_message():
    """Generate unsupported message for the run script attempt"""
    return "\n".join((
        get_unsupported_title(action="run"),
        "Try running:",
        "    $ python3 {package_name}",
    )).format(package_name=info.PACKAGE_NAME)


def check_version(message):
    """Check if current version is supported"""
    if _CURRENT_VERSION < info.PYTHON_MIN_VERSION:
        sys.exit(
            "{error_color}{message}{default_color}".format(
                error_color=ERROR_COLOR,
                message=message,
                default_color=DEFAULT_COLOR,
            )
        )


def check_if_can_execute():
    """
    doc
    """
    check_version(message=get_unsupported_execution_message())


def check_if_can_install():
    """
    doc
    """
    check_version(message=get_unsupported_installation_message())
