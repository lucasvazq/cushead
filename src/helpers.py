#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc
"""

import pathlib
from typing import Iterable, Tuple, NamedTuple


class Image(NamedTuple):
    """
    doc
    """
    reference: str
    name: str
    data: bytes


def get_images_list() -> Tuple[Image]:
    """
    doc
    """
    assets_path = pathlib.Path(pathlib.Path(__file__).parent, 'assets')
    assets = (
        ('favicon_ico', 'favicon_ico_16px.ico'),
        ('favicon_png', 'favicon_png_1600px.png'),
        ('favicon_svg', 'favicon_svg_scalable.svg'),
        ('preview_png', 'preview_png_500px.png'),
    )
    return tuple(
        Image(
            reference=reference,
            name=(assets_path / filename).name,
            data=(assets_path / filename).read_bytes(),
        )
        for reference, filename in assets
    )


def string_list_union(
    *,
    string_list: Iterable[str],
) -> str:
    """
    Return a iterable represented into a sentence

    Example:
        input = ["foo", "bar", "baz", "etc"]
        output = "foo, bar, baz and etc"
    """
    return " and ".join(", ".join(string_list).rsplit(", ", 1))
