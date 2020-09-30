#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script
"""
import setuptools

from src import info
from src import support


support.check_if_can_install()


with open("README.md", "r") as fh:
    _LONG_DESCRIPTION = fh.read()
setuptools.setup(
    name=info.PACKAGE_NAME,
    version=info.PACKAGE_VERSION,
    scripts=["{}.py".format(info.PACKAGE_NAME)],
    entry_points={
        "console_scripts": ["{0}={0}:main".format(info.PACKAGE_NAME)]
    },
    url=info.SOURCE,
    project_urls={
        "Documentation": info.DOCUMENTATION,
        "Source": info.SOURCE,
    },
    python_requires=">={}.{}".format(*(info.PYTHON_MIN_VERSION)),
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=info.REQUIRED_PACKAGES,
    author=info.AUTHOR,
    author_email=info.EMAIL,
    description=info.DESCRIPTION,
    long_description=_LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license=info.PACKAGE_LICENSE,
    keywords=info.KEYWORDS,
    platforms="any",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
