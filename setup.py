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
    name=info.package_name,
    version=info.package_version,
    scripts=["{}.py".format(info.package_name)],
    entry_points={
        "console_scripts": ["{0}={0}:main".format(info.package_name)]
    },
    url=info.source,
    project_urls={
        "Documentation": info.documentation,
        "Source": info.source,
    },
    python_requires=">={}.{}".format(*(info.python_min_version)),
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=info.required_packages,
    author=info.author,
    author_email=info.email,
    description=info.description,
    long_description=_LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license=info.package_license,
    keywords=info.keywords,
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
