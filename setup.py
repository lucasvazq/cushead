#!/usr/bin/env python3
"""
Host the setup function.
"""
import pathlib

import setuptools

from cushead import info


def setup():
    """
    Execute the setup.
    """
    assets_path = pathlib.Path(info.PACKAGE_NAME) / "console" / "assets" / "images"
    templates_path = pathlib.Path(info.PACKAGE_NAME) / "generator" / "templates" / "jinja" / "templates"

    setuptools.setup(
        name=info.PACKAGE_NAME,
        version=info.PACKAGE_VERSION,
        entry_points={"console_scripts": [f"{info.PACKAGE_NAME}={info.PACKAGE_NAME}.console.console:main"]},
        url=info.SOURCE,
        project_urls={
            "Documentation": info.DOCUMENTATION,
            "Source": info.SOURCE,
        },
        python_requires=f">={info.PYTHON_MIN_VERSION[0]}.{info.PYTHON_MIN_VERSION[1]}",
        packages=setuptools.find_packages(exclude=(file.name for file in pathlib.Path("").iterdir() if file.name != info.PACKAGE_NAME)),
        include_package_data=True,
        data_files=[
            ("", ["requirements.txt", "LICENSE.md", "README.md"]),
            (assets_path, [str(file) for file in pathlib.Path(assets_path).iterdir()]),
            (templates_path, [str(file) for file in pathlib.Path(templates_path).iterdir()]),
        ],
        zip_safe=False,
        install_requires=pathlib.Path("requirements.txt").read_text().split(),
        author=info.AUTHOR,
        author_email=info.EMAIL,
        description=info.DESCRIPTION,
        long_description=pathlib.Path("README.md").read_text(),
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
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Utilities",
            "Topic :: Software Development",
            "Topic :: Software Development :: Code Generators",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Software Development :: User Interfaces",
        ],
    )


if __name__ == "__main__":
    setup()
