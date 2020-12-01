"""
Handle files generation.
"""
import pathlib
from typing import NamedTuple
from typing import Tuple

from cushead.generator import config as generator_config
from cushead.generator import images
from cushead.generator.templates import templates


class File(NamedTuple):
    """
    Store data about a file to create.
    """

    path: pathlib.Path
    data: bytes


def generate_files(*, config: generator_config.Config) -> Tuple[File, ...]:
    """
    Get the images and templates to create.

    Args:
        config: the config.

    Returns:
        The images and templates.
    """
    return (
        *images.generate_images(config=config),
        *templates.generate_templates(config=config),
    )
