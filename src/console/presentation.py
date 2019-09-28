#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to handle the presentation of the package

Relevant Global Variables:
    PRESENTATION_MESSAGE str: The presentation of the package, include a big
        logo in ASCII and info about the author and the package
"""

import textwrap

from src.info import get_info


INFO = get_info()


# Console output in /docs/console.png
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
    INFO['package_version'],
    INFO['author'],
    INFO['email'],
    INFO['author_page'],
    INFO['license'],
    INFO['source'],
    INFO['documentation'],
    INFO['package_name'],
)
