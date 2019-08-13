#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.support import Support
Support().install()

import sys

import setuptools

from _info import get_info


INFO = get_info()


with open('README.md', 'r') as fh:
    long_description = fh.read()
setuptools.setup(
    name=INFO['name'],
    version=INFO['version'],
    url=INFO['source'],
    project_urls={
        'Documentation': INFO['documentation'],
        'Source': INFO['source']
    },
    python_requires=">={}.{}, <{}.{}".format(*(INFO['python_min_version'] +
        INFO['python_max_version'])),
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
