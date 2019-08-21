#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import textwrap

from .info import Info
INFO = Info().get_info()


(DEFAULT_COLOR, ERROR_COLOR, PRESENTATION_COLOR) = (
    ('', '', '')
    if os.name == 'nt' else
    (
        '\033[0;0m',  # DEFAULT
        '\033[1;31m',  # ERROR: Red
        '\033[1;34m'  # PRESENTATION: Blue
    )
)


# Console output in /doc/presentation.png
PRESENTATION_MESSAGE = textwrap.dedent("""\
       {}____  _   _  ____   _   _  _____     _     ____     ____ __   __
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
    {}""")  # This line is blank
PRESENTATION_MESSAGE = PRESENTATION_MESSAGE.format(
    PRESENTATION_COLOR,
    INFO['package_version'],
    INFO['author'],
    INFO['email'],
    INFO['author_page'],
    INFO['license'],
    INFO['source'],
    INFO['documentation'],
    INFO['package_name'],
    DEFAULT_COLOR
)
