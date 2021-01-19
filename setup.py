#!/usr/bin/env python3
"""
Setup script.
"""
import pathlib

import setuptools

from cushead import info


def setup():
    assets_path = pathlib.Path(f"{info.PACKAGE_NAME}") / "console" / "assets" / "images"
    templates_path = pathlib.Path(f"{info.PACKAGE_NAME}") / "generator" / "templates" / "jinja" / "templates"
    docs_path = pathlib.Path("docs")

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
        packages=setuptools.find_packages(exclude=("tests",)),
        include_package_data=True,
        data_files=[
            ("", ["requirements.txt", "LICENSE.md", "README.md"]),
            (docs_path, [str(docs_path / "logo.png")]),
            (assets_path, [str(file) for file in pathlib.Path(assets_path).iterdir()]),
            (templates_path, [str(file) for file in pathlib.Path(templates_path).iterdir()]),
        ],
        zip_safe=False,
        install_requires=info.REQUIRED_PACKAGES,
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
        ],
    )


if __name__ == "__main__":
    setup()
