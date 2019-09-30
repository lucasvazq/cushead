#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Handle logs information

Relevant Global Variables:
    PRESENTATION_MESSAGE str: The presentation of the package, include a big
        logo in ASCII and info about the author and the package

Classes:
    SpecialMessages
"""

import sys

from src.helpers.strings import ColorProcessor

import textwrap

from src.info import Info


_INFO = Info.get_info()

# presentation is in /docs/presentation.png
PRESENTATION_MESSAGE = textwrap.dedent("""\
       ____  _   _  ____   _   _  _____     _     ____     ____ __   __
      / ___|| | | |/ ___| | | | || ____|   / \\   |  _ \\   |  _ \\\\ \\ / /
     | |    | | | |\\___ \\ | |_| ||  _|    / _ \\  | | | |  | |_) |\\ V / 
     | |___ | |_| | ___) ||  _  || |___  / ___ \\ | |_| |_ |  __/  | |  
      \\____| \\___/ |____/ |_| |_||_____|/_/   \\_\\|____/(_)|_|     |_|  
                                 __       _
                                 _/     /
                                /    __/
             UX / SEO         _/  __/           v {}
                             / __/
                            / /
                           /'

    Author: {}
    Email: {}
    Page: {}
    License: {}

    Git: {}
    Documentation: {}
    For help run: {} -h
    """)  # This line is blank
PRESENTATION_MESSAGE = PRESENTATION_MESSAGE.format(
    _INFO['package_version'],
    _INFO['author'],
    _INFO['email'],
    _INFO['author_page'],
    _INFO['license'],
    _INFO['source'],
    _INFO['documentation'],
    _INFO['package_name'],
)


class SpecialMessages:

    @staticmethod
    def presentation_message():
        return PRESENTATION_MESSAGE


class MessagesHandler:

    # error section

    def error_exception(self, message: str = ''):
        raise Exception(message)

    def error_stdout(self, message: str = ''):
        class_instance = ColorProcessor(message)
        sys.exit(class_instance.error_color())

    # important section

    def important_stdout(self, message: str = ''):
        class_instance = ColorProcessor(message)
        sys.stdout.write(class_instance.important_color())

    # normal section

    def normal_stdout(self, message: str = ''):
        class_instance = ColorProcessor(message + '\n')
        sys.stdout.write(class_instance.normal_color())


class Logs(MessagesHandler):
    error_function = MessagesHandler.error_exception
    important_function = MessagesHandler.important_stdout

    def error(self, message):
        self.error_function(message)

    def important(self, message):
        self.important_function(message)

