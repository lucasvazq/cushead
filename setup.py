#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from _info import get_info
INFO = get_info()
CURRENT_PYTHON = sys.version_info[:2]
MIN_PYTHON = INFO['python_min_version']
MAX_PYTHON = INFO['python_max_version']
MESSAGE = """
==========================
Unsupported Python version
==========================
This version of cushead.py requires Python >={}.{} and <{}.{}, but you're trying to
install it with Python {}.{}.
Make sure you have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
    $ python3 -m pip install cushead.py
This will update pip and setuptools, and install the latest version of
cushead.py, make sure you still trying to install and running it with a
version of Python that is >=3.5 and <4.
""".format(*(MIN_PYTHON + MAX_PYTHON + CURRENT_PYTHON))
if CURRENT_PYTHON < MIN_PYTHON or CURRENT_PYTHON >= MAX_PYTHON:
    sys.stderr.write(MESSAGE)
    sys.exit(1)

import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()
setuptools.setup(
    name=INFO['name'],
    version=INFO['version'],
    url=INFO['source'],
    project_urls={
        'Documentation': INFO['remote_documentation'],
        'Source': INFO['source']
    },
    python_requires=">={}.{}, <{}.{}".format(*(MIN_PYTHON + MAX_PYTHON)),
    packages=setuptools.find_packages(),
    install_requires=INFO['required_packages'],
    author=INFO['author'],
    author_email=INFO['email'],
    description=INFO['description'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=INFO['license'],
    keywords='SEO, UX, front-end',
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
