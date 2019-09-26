#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Handle logs information"""

import sys

from src.helpers.miscellaneous import void_function
from src.support import ERROR_COLOR, DEFAULT_COLOR


def error_message_processor(message: str) -> str:
    return ERROR_COLOR + message + DEFAULT_COLOR


def stdout_error_report(message: str, processor: callable = void_function):
    sys.exit(processor(message))


def exception_error_report(message: str, processor: callable = void_function):
    raise Exception(processor(message))
