"""
Informative module.
"""
import pathlib


_REQUIREMENTS_FILE = pathlib.Path(__file__).parent.parent / 'requirements.txt'


PACKAGE_NAME = "cushead"
PACKAGE_VERSION = "3.1.8"
PYTHON_MIN_VERSION = (3, 8)
SOURCE = f"https://github.com/lucasvazq/{PACKAGE_NAME}"
DOCUMENTATION = f"https://github.com/lucasvazq/{PACKAGE_NAME}/blob/master/README.md"
REQUIRED_PACKAGES = _REQUIREMENTS_FILE.read_text().split()
AUTHOR = "Lucas Vazquez"
EMAIL = "lucas5zvazquez@gmail.com"
DESCRIPTION = "CLI that help you to improve the SEO and UX of your websites."
PACKAGE_LICENSE = "MIT"
KEYWORDS = "SEO, meta-tags, UX, PWA, front-end, favicon, manifest, robots, browserconfig, sitemap, opensearch"
AUTHOR_PAGE = "https://github.com/lucasvazq"
