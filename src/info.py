#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Informative module"""

# IMPORTANT: This module would be python2 and python3 compatible

from collections import namedtuple


__package_name__ = "cushead"
__package_version__ = "3.1.8"
__source__ = "https://github.com/lucasvazq/{}".format(__package_name__)
__documentation__ = "https://github.com/lucasvazq/{}/blob/master/README.md".format(__package_name__)
__python_min_version__ = (
    3,
    7,
)
__required_packages__ = (
    "python-resize-image",
    "Pillow",
)
__author__ = "Lucas Vazquez"
__author_page__ = "https://github.com/lucasvazq"
__email__ = "lucas5zvazquez@gmail.com"
__description__ = "CLI that help you to improve the SEO and UX of your websites."
__license__ = "MIT"
__keywords__ = "SEO, meta-tags, UX, PWA, front-end, favicon, manifest, robots, browserconfig, sitemap, opensearch"
__copyright__ = "{} © 2020 {}. Released under the MIT License.".format(
    __package_name__,
    __author__,
)
__maintainer__ = "Lucas Vazquez"
__status__ = "Production"


def get_info():
    """
    Return the info
    
    Returns:
        ...
    """
    return namedtuple(
        typename='Info',
        field_names=(
            "package_name",
            "package_version",
            "source",
            "documentation",
            "python_min_version",
            "required_packages",
            "author",
            "author_page",
            "email",
            "description",
            "license",
            "keywords",
            "copyright",
            "maintainer",
            "status",
        )
    )(
        package_name=__package_name__,
        package_version=__package_version__,
        source=__source__,
        documentation=__documentation__,
        python_min_version=__python_min_version__,
        required_packages=__required_packages__,
        author=__author__,
        author_page=__author_page__,
        email=__email__,
        description=__description__,
        license=__license__,
        keywords=__keywords__,
        copyright=__copyright__,
        maintainer=__maintainer__,
        status=__status__,
    )
