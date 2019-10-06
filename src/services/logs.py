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


class MessagesHandler:
    """Handle different types of outputs

    Methods:
        @staticmethod default_stdout
        @staticmethod error_exception
        @staticmethod error_stdout
        @staticmethod presentation_stdout
    """

    # default section

    @staticmethod
    def default_stdout(message: str = ''):
        class_instance = ColorProcessor(message + '\n')
        sys.stdout.write(class_instance.default_color())

    # error section

    @staticmethod
    def error_exception(message: str = ''):
        raise Exception(message)

    @staticmethod
    def error_stdout(message: str = ''):
        class_instance = ColorProcessor(message)
        sys.exit(class_instance.error_color())

    # presentation section

    @staticmethod
    def presentation_stdout(message: str = ''):
        class_instance = ColorProcessor(message + '\n')
        sys.stdout.write(class_instance.presentation_color())


class Logs(MessagesHandler):
    """Different output handler for different situations
    
    Methods:
        default_log
        error_log
        presentation_log
    """

    def default_log(self, message: str = ''):
        self.default_stdout(message)

    def error_log(self, message: str = ''):
        self.error_exception(message)

    def presentation_log(self, message: str = ''):
        self.presentation_stdout(message)


class SpecialMessages:
    """Special messages class

    Methods:
        @staticmethod presentation_message
    """

    @staticmethod
    def presentation_message():
        return PRESENTATION_MESSAGE
