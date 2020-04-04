#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup script"""
import sys

import setuptools

import src_2.info
import src_2.support

# Check python version
try:
    _INFO = src_2.info.get_info()
    src_2.support.Support(_INFO).check_for_installation()
except src_2.support.Unsupported as exception:
    sys.stdout.write(exception)
    sys.exit()


with open("README.md", "r") as fh:
    _LONG_DESCRIPTION = fh.read()
_PYTHON_REQUIRES = ">={}.{}, <{}.{}"
_PYTHON_REQUIRES = _PYTHON_REQUIRES.format(
    *(_INFO["python_min_version"] + _INFO["python_max_version"])
)
setuptools.setup(
    name=_INFO["package_name"],
    version=_INFO["package_version"],
    scripts=[f"{_INFO['package_name']}.py"],
    entry_points={
        "console_scripts": ["{0}={0}:main".format(_INFO["package_name"])]
    },
    url=_INFO["source"],
    project_urls={
        "Documentation": _INFO["documentation"],
        "Source": _INFO["source"],
    },
    python_requires=_PYTHON_REQUIRES,
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=_INFO["required_packages"],
    author=_INFO["author"],
    author_email=_INFO["email"],
    description=_INFO["description"],
    long_description=_LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license=_INFO["license"],
    keywords=_INFO["keywords"],
    platforms="any",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
