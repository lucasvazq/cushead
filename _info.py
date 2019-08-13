#!/usr/bin/env python
# -*- coding: utf-8 -*-


# used for setup.py
__name__ = "cushead.py"
__version__ = "3.0.0"
__source__ = "https://github.com/lucasvazq/cushead.py"
__documentation__ = "https://github.com/lucasvazq/cushead.py/blob/master/README.md"
__python_min_version__ = (3, 5)
__python_max_version__ = (4, 0)
__required_packages__ = ['argparse', 'python-resize-image']
__author__ = "Lucas Vazquez"
__author_page__ = "https://github.com/lucasvazq"
__email__ = "lucas5zvazquez@gmail.com"
__description__ = "CLI that help you to improve the SEO and UX of your websites."
__license__ = "MIT"
__keywords__ = ("SEO, meta-tags, UX, PWA, front-end, favicon, manifest, " +
    "robots, browserconfig, sitemap, opensearch")

# others
__copyright__ = """\
{} © 2019 {}. Released under the MIT License.""".format(__name__, __author__)
__maintainer__ = "Lucas Vazquez"

__status__ = "Production"

def get_info():
    return {
        'name': __name__,
        'version': __version__,
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
