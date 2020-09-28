#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc
"""
import sys
import textwrap
from typing import NoReturn

from src import info
from src import support



PRESENTATION_MESSAGE = textwrap.dedent(f"""\
       ____  _   _  ____   _   _  _____     _     ____     ____ __   __
      / ___|| | | |/ ___| | | | || ____|   / \\   |  _ \\   |  _ \\\\ \\ / /
     | |    | | | |\\___ \\ | |_| ||  _|    / _ \\  | | | |  | |_) |\\ V /
     | |___ | |_| | ___) ||  _  || |___  / ___ \\ | |_| |_ |  __/  | |
      \\____| \\___/ |____/ |_| |_||_____|/_/   \\_\\|____/(_)|_|     |_|
                                 __       _
                                 _/     /
                                /    __/
             UX / SEO         _/  __/           v {info.package_version}
                             / __/
                            / /
                           /'

    Author: {info.author}
    Email: {info.email}
    Page: {info.author_page}
    License: {info.package_license}

    Source: {info.source}
    Documentation: {info.documentation}
    For help run: {info.package_name} -h
""")


def log(*, color: str, message: str, is_exit: bool) -> NoReturn:
    """
    doc
    """
    function = sys.exit if is_exit else sys.stdout.write
    function(f"{color}{message}{support.DEFAULT_COLOR}\n")


def error_log(*, message: str) -> NoReturn:
    """
    doc
    """
    log(
        color=support.ERROR_COLOR,
        message=message,
        is_exit=True
    )


def default_log(*, message: str) -> NoReturn:
    """
    doc
    """
    log(
        color=support.DEFAULT_COLOR,
        message=message,
        is_exit=False,
    )


def presentation_log(*, message: str) -> NoReturn:
    """
    doc
    """
    log(
        color=support.PRESENTATION_COLOR,
        message=message,
        is_exit=False,
    )
