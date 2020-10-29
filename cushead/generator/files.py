"""
Handle files generation.
"""
import pathlib
from typing import NamedTuple
from typing import Tuple

from cushead.generator import configuration
from cushead.generator import images
from cushead.generator.templates import templates


class File(NamedTuple):
    """
    Used to store data about a file that want to create.
    """

    path: pathlib.Path
    data: bytes


def generate_files(*, config: configuration.Config) -> Tuple[File, ...]:
    """
    Get the images and templates to create.

    Args:
        config: the configuration.

    Returns:
        The list of images and templates.
    """
    return (
        *images.generate_images(config=config),
        *templates.generate_templates(config=config),
    )
