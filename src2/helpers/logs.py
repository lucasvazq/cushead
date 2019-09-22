#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Handle logs information"""

import os
import sys


(DEFAULT_COLOR, ERROR_COLOR, CONSOLE_PRESENTATION_COLOR) = (
    ('', '', '')
    if os.name == 'nt' else
    (
        '\033[0;0m',  # DEFAULT
        '\033[1;31m',  # ERROR: Red
        '\033[1;34m'  # CONSOLE PRESENTATION: Blue
    )
)


def error_message(message):
    """Print error message"""
    raise Exception(message)
    sys.exit(ERROR_COLOR + message + DEFAULT_COLOR)
