#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

CURRENT_PYTHON = sys.version_info[:2]
MIN_PYTHON = (3, 5)
MAX_PYTHON = (4, 0)
if CURRENT_PYTHON < MIN_PYTHON or CURRENT_PYTHON > MAX_PYTHON:
    err = True
else:
    err = False
if err:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of cushead.py requires Python >=3.5 and <4, but you're trying to
install it with Python {}.{}.
Make sure you have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
    $ python3 -m pip install cushead.py
This will update pip and setuptools, and install the latest version of
cushead.py, make sure you still trying to install and running it with a
version of Python that is >=3.5 and <4.
""".format(
        *(CURRENT_PYTHON))
    )
    sys.exit(1)

from importlib import machinery
from os import getcwd
from os.path import join
import types

import setuptools


# Obtain version
def get_version(file):

    name = file
    file = join(getcwd(), file)

    loader = machinery.SourceFileLoader(name, file)
    mod = types.ModuleType(loader.name)
    loader.exec_module(mod)

    return mod.__version__


with open('README.md', 'r') as fh:
    long_description = fh.read()
setuptools.setup(
    name='cushead.py',
    scripts=['__main__.py', '_version.py', 'setup.py'],
    version=get_version('./_version.py'),
    url='https://github.com/lucasvazq/cushead.py',
    project_urls={
        'Documentation': 'https://github.com/lucasvazq/cushead.py/blob/master/README.md',
        'Source': 'https://github.com/lucasvazq/cushead.py'
    },
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
    license='MIT',
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
