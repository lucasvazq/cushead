#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import textwrap

from .info import Info
INFO = Info.get_info()


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
PRESENTATION_MESSAGE = textwrap.dedent(f"""{PRESENTATION_COLOR}\
       ____  _   _  ____   _   _  _____     _     ____     ____ __   __
      / ___|| | | |/ ___| | | | || ____|   / \\   |  _ \\   |  _ \\\\ \\ / /
     | |    | | | |\\___ \\ | |_| ||  _|    / _ \\  | | | |  | |_) |\\ V / 
     | |___ | |_| | ___) ||  _  || |___  / ___ \\ | |_| |_ |  __/  | |  
      \\____| \\___/ |____/ |_| |_||_____|/_/   \\_\\|____/(_)|_|     |_|  
                                 __       _
                                 _/     /
                                /    __/
             UX / SEO         _/  __/           v {INFO['package_version']}
                             / __/
                            / /
                           /'

    Author: {INFO['author']}
    Email: {INFO['email']}
    Page: {INFO['author_page']}
    License: {INFO['license']}

    Git: {INFO['source']}
    Documentation: {INFO['documentation']}
    For help run: {INFO['package_name']} -h
    {DEFAULT_COLOR}""")  # This line is blank
