#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import sys

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 5)
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of cushead.py requires Python {}.{}, but you're trying to install 
it on Python {}.{}.
Make sure you have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
    $ python3 -m pip install cushead.py
This will update pip and setuptools, and install the latest version of
cushead.py which works on your computer.""".format(
        *(REQUIRED_PYTHON + CURRENT_PYTHON))
    )
    sys.exit(1)

with open('README.md', 'r') as fh:
    long_description = fh.read()
setuptools.setup(
    name='cushead.py',
    scripts=['cushead.py'],
    version='2.3.2',
    url='https://github.com/lucasvazq/cushead.py',
    project_urls={
        'Documentation': 'https://docs.djangoproject.com/',
        'Source': 'https://github.com/django/django',
    }
    python_requires='>=3.5, <4',
    packages=setuptools.find_packages(),
    install_requires=['argparse'],
    author='Lucas Vazquez',
    author_email='lucas5zvazquez@gmail.com',
    description=
        "This simple script improve your SEO and UX. " +
        "It add lang attribute to the html element and search and replace " +
        "'$head$' string with personalized head elements.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='SEO, UX, front-end',
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
        'Programming Language :: Python :: 3 :: Only',
    ]
)
