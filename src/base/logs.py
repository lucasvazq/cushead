#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Handle logs information

Relevant Global Variables:
    PRESENTATION_MESSAGE str: The presentation of the package, include a big
        logo in ASCII and info about the author and the package

Classes:
    MessagesHandler
    Logs
    SpecialMessages
"""
import os
import sys
import textwrap
from typing import NoReturn

from src import info
from src import support


_INFO = info.get_info()


# presentation is in /docs/presentation.png
PRESENTATION_MESSAGE = textwrap.dedent(f"""\
       ____  _   _  ____   _   _  _____     _     ____     ____ __   __
      / ___|| | | |/ ___| | | | || ____|   / \\   |  _ \\   |  _ \\\\ \\ / /
     | |    | | | |\\___ \\ | |_| ||  _|    / _ \\  | | | |  | |_) |\\ V /
     | |___ | |_| | ___) ||  _  || |___  / ___ \\ | |_| |_ |  __/  | |
      \\____| \\___/ |____/ |_| |_||_____|/_/   \\_\\|____/(_)|_|     |_|
                                 __       _
                                 _/     /
                                /    __/
             UX / SEO         _/  __/           v {_INFO.package_version}
                             / __/
                            / /
                           /'

    Author: {_INFO.author}
    Email: {_INFO.email}
    Page: {_INFO.author_page}
    License: {_INFO.license}

    Source: {_INFO.source}
    Documentation: {_INFO.documentation}
    For help run: {_INFO.package_name} -h
""")


def log(
    *,
    color: str,
    message: str,
    is_exit: bool,
) -> NoReturn:
    """
    doc
    """
    function = sys.exit if is_exit else sys.stdout.write
    function(f"{color}{message}{support.DEFAULT_COLOR}\n")


def error_log(
    *,
    message: str,
) -> NoReturn:
    """
    doc
    """
    log(
        color=support.ERROR_COLOR,
        message=message,
        is_exit=True
    )


def default_log(
    *,
    message: str,
) -> NoReturn:
    """
    doc
    """
    log(
        color=support.DEFAULT_COLOR,
        message=message,
        is_exit=False,
    )


def presentation_log(
    *,
    message: str,
) -> NoReturn:
    """
    doc
    """
    log(
        color=support.PRESENTATION_COLOR,
        message=message,
        is_exit=False,
    )
