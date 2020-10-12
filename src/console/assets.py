"""
Module to handle the assets.
"""
import pathlib
from typing import NamedTuple


class Image(NamedTuple):
    """
    Used to store data of the assets images.
    """

    name: str
    data: bytes


class Assets(NamedTuple):
    """
    Store data about images assets.
    """

    favicon_ico: Image
    favicon_png: Image
    favicon_svg: Image
    preview_png: Image


def get_assets_images() -> Assets:
    """
    Get the assets images.

    Returns:
        A tuple of the images.
    """
    assets_path = pathlib.Path(__file__).parent / "assets"
    return Assets(
        favicon_ico=Image(name="favicon_ico_16px.ico", data=(assets_path / "favicon_ico_16px.ico").read_bytes()),
        favicon_png=Image(name="favicon_png_2688px.png", data=(assets_path / "favicon_png_2688px.png").read_bytes()),
        favicon_svg=Image(name="favicon_svg_scalable.svg", data=(assets_path / "favicon_svg_scalable.svg").read_bytes()),
        preview_png=Image(name="preview_png_600px.png", data=(assets_path / "preview_png_600px.png").read_bytes()),
    )
