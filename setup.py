#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()
setuptools.setup(
    name='cushead.py',
    version='2.3.1',
    scripts=['cushead.py'],
    install_requires=[
        'argparse'
    ],
    author='Lucas Vazquez',
    author_email='lucas5zvazquez@gmail.com',
    description=
        "This simple script improve your SEO and UX. " +
        "It add lang attribute to the html element and search and replace " +
        "'$head$' string with personalized head elements.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='SEO, UX, front-end',
    url='https://github.com/lucasvazq/cushead.py',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5, <4',
    install_requires=['argparse']
)
