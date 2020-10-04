"""
Helpers.
"""
import pathlib
from collections import namedtuple
from typing import Iterable
from typing import NamedTuple
from typing import Tuple


class Image(NamedTuple):
    """
    Used to store data of the assets images.
    """

    reference: str
    name: str
    data: bytes


def get_assets_list() -> Tuple[Image]:
    """
    Get the assets images.

    Returns:
        A tuple of the images.
    """
    ImageReference = namedtuple('ImageReference', 'reference name')
    assets = (
        ImageReference(reference='favicon_ico', name='favicon_ico_16px.ico'),
        ImageReference(reference='favicon_png', name='favicon_png_1600px.png'),
        ImageReference(reference='favicon_svg', name='favicon_svg_scalable.svg'),
        ImageReference(reference='preview_png', name='preview_png_500px.png'),
    )
    assets_path = pathlib.Path(pathlib.Path(__file__).parent, 'assets')
    return tuple(
        Image(
            reference=reference,
            name=(assets_path / filename).name,
            data=(assets_path / filename).read_bytes(),
        )
        for reference, filename in assets
    )


def string_list_union(*, string_list: Iterable[str]) -> str:
    """
    Return a iterable represented into a sentence.

    Args:
        string_list: the iterable.

    Returns:
        The sentence.

    Example:
        input = ["foo", "bar", "baz", "etc"]
        output = "foo, bar, baz and etc"
    """
    return " and ".join(", ".join(string_list).rsplit(", ", 1))
