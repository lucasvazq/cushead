"""
Get assets files.
"""
import pathlib
from typing import NamedTuple


class Image(NamedTuple):
    """
    Store image data.
    """

    name: str
    data: bytes


class Assets(NamedTuple):
    """
    Store assets data.
    """

    favicon_ico: Image
    favicon_png: Image
    favicon_svg: Image
    preview_png: Image


def get_images() -> Assets:
    """
    Get the assets images.

    Returns:
        A tuple of the images.
    """
    assets_folder = pathlib.Path(__file__).parent / "images"
    return Assets(
        Image("favicon_ico_16px.ico", (assets_folder / "favicon_ico_16px.ico").read_bytes()),
        Image("favicon_png_2688px.png", (assets_folder / "favicon_png_2688px.png").read_bytes()),
        Image("favicon_svg_scalable.svg", (assets_folder / "favicon_svg_scalable.svg").read_bytes()),
        Image("preview_png_600px.png", (assets_folder / "preview_png_600px.png").read_bytes()),
    )
