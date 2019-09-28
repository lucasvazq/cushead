#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Handle logs information"""

import sys

from src.support import CONSOLE_PRESENTATION_COLOR, DEFAULT_COLOR, ERROR_COLOR


class MessageHandler:

    # important section

    @staticmethod
    def important_stdout(message: str):
        print(CONSOLE_PRESENTATION_COLOR + message + DEFAULT_COLOR)

    # error section

    @staticmethod
    def error_exception(message: str):
        raise Exception(message)

    @staticmethod
    def error_stdout(message: str):
        sys.exit(ERROR_COLOR + message + DEFAULT_COLOR)


class Logs:
    error_function = MessageHandler.error_exception
    important_function = MessageHandler.important_stdout

    def important(self, message):
        self.important_function(message)

    def error(self, message):
        self.error_function(message)
