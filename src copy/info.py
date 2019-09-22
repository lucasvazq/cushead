#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Informative module"""

# Keep the old style format

# Used for setup and main script
__package_name__ = "cushead"
__package_version__ = "3.1.8"
__source__ = "https://github.com/lucasvazq/{}".format(__package_name__)
__documentation__ = ("https://github.com/lucasvazq/{}/blob/master/README.md"
                     .format(__package_name__))
__python_min_version__ = (3, 5)
__python_max_version__ = (4, 0)
__required_packages__ = ['argparse', 'python-resize-image', 'Pillow']
__author__ = "Lucas Vazquez"
__author_page__ = "https://github.com/lucasvazq"
__email__ = "lucas5zvazquez@gmail.com"
__description__ = ("CLI that help you to improve the SEO and UX of your "
                   "websites.")
__license__ = "MIT"
__keywords__ = ("SEO, meta-tags, UX, PWA, front-end, favicon, manifest, " +
                "robots, browserconfig, sitemap, opensearch")

# Unused
__copyright__ = ("{} © 2019 {}. Released under the MIT License."
                 .format(__package_name__, __author__))
__maintainer__ = "Lucas Vazquez"
__status__ = "Production"


def get_info():
    """Return the info"""
    info = {
        'package_name': __package_name__,
        'package_version': __package_version__,
        'source': __source__,
        'documentation': __documentation__,
        'python_min_version': __python_min_version__,
        'python_max_version': __python_max_version__,
        'required_packages': __required_packages__,
        'author': __author__,
        'author_page': __author_page__,
        'email': __email__,
        'description': __description__,
        'license': __license__,
        'keywords': __keywords__
    }
    return info
