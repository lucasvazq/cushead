#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()
setuptools.setup(
    name='cushead.py',
    version='2.3.1',
    scripts=['cushead.py'],
    author='Lucas Vazquez',
    author_email='lucas5zvazquez@gmail.com',
    description=
        "This simple script improve your SEO and UX. " +
        "It add lang attribute to the html element and search and replace " +
        "'$head$' string with personalized head elements.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lucasvazq/cushead.py',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
