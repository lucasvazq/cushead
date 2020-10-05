#!/usr/bin/env python3
"""
Setup script.
"""
import setuptools

from src import info


with open("README.md", "r") as fh:
    _LONG_DESCRIPTION = fh.read()
setuptools.setup(
    name=info.PACKAGE_NAME,
    version=info.PACKAGE_VERSION,
    scripts=[f"{info.PACKAGE_NAME}.py"],
    entry_points={"console_scripts": [f"{info.PACKAGE_NAME}={info.PACKAGE_NAME}:main"]},
    url=info.SOURCE,
    project_urls={
        "Documentation": info.DOCUMENTATION,
        "Source": info.SOURCE,
    },
    python_requires=f">={info.PYTHON_MIN_VERSION[0]}.{info.PYTHON_MIN_VERSION[1]}",
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
