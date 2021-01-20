"""
Store package information.
"""
import pathlib

PACKAGE_NAME = "cushead"
PACKAGE_VERSION = "4.0.3"
PYTHON_MIN_VERSION = (3, 8)
SOURCE = f"https://github.com/lucasvazq/{PACKAGE_NAME}"
DOCUMENTATION = f"https://github.com/lucasvazq/{PACKAGE_NAME}/blob/master/README.md"
AUTHOR = "Lucas Vazquez"
EMAIL = "lucas5zvazquez@gmail.com"
DESCRIPTION = "CLI that help you to improve the SEO and UX of your websites."
PACKAGE_LICENSE = "MIT"
KEYWORDS = "SEO, meta-tags, UX, PWA, front-end, favicon, manifest, robots, browserconfig, sitemap, opensearch"
AUTHOR_PAGE = "https://github.com/lucasvazq"

if (pathlib.Path(__file__).parent / "requirements.txt").exists():
    # Used in build context.
    REQUIRED_PACKAGES = (pathlib.Path(__file__).parent / "requirements.txt").read_text().split()
else:
    # Used in develop and testing context.
    REQUIRED_PACKAGES = (pathlib.Path(__file__).parent.parent / "requirements.txt").read_text().split()
