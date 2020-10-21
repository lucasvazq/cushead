"""
Handle images generation.
"""
from __future__ import annotations

import collections
import io
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from typing import overload

from PIL import IcoImagePlugin
from PIL import Image
from PIL import ImageColor
from PIL import PngImagePlugin
from resizeimage import resizeimage

from src.generator import configuration
from src.generator import files


@overload
def resize_image(*, image: None, width: int, height: int) -> None:
    ...


@overload
def resize_image(*, image: IcoImagePlugin.IcoImageFile, width: int, height: int) -> IcoImagePlugin.IcoImageFile:
    ...


@overload
def resize_image(*, image: PngImagePlugin.PngImageFile, width: int, height: int) -> PngImagePlugin.PngImageFile:
    ...


def resize_image(*, image, width, height):
    """
    Return a image resized.

    Args:
        image: a PIL image instance.
        width: the width.
        height : the height.

    Returns:
        A new image resized.
    """
    if image is None:
        return None

    resized_image = resizeimage.resize_contain(image, (width, height))
    resized_image.format = image.format
    return resized_image


@overload
def remove_transparency(*, image: None, background_color: str) -> None:
    ...


@overload
def remove_transparency(*, image: IcoImagePlugin.IcoImageFile, background_color: str) -> IcoImagePlugin.IcoImageFile:
    ...


@overload
def remove_transparency(*, image: PngImagePlugin.PngImageFile, background_color: str) -> PngImagePlugin.PngImageFile:
    ...


def remove_transparency(*, image, background_color):
    """
    Remove the transparency of png images.

    Args:
        image: a PIL image instance.
        background_color: the background color used to replace the transparency.

    Returns:
        A PIL image instance.
    """
    if image is None:
        return None

    # Remove transparency (https://stackoverflow.com/a/35859141/10712525)
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        alpha = image.convert("RGBA").getchannel("A")
        color = ImageColor.getrgb(background_color) + (255,)
        new_image = Image.new("RGBA", image.size, color)
        new_image.paste(image, mask=alpha)
        new_image.format = image.format
        return new_image
    return image


def read_image_bytes(image: Optional[Union[IcoImagePlugin.IcoImageFile, PngImagePlugin.PngImageFile]]) -> bytes:
    """
    Read the bytes of a image.

    Args:
        image: a PIL image instance

    Returns:
        The bytes data.
    """
    if image is None:
        return bytes()

    io_file = io.BytesIO()
    image.save(io_file, format=image.format)
    return io_file.getvalue()


def generate_images(*, config: configuration.Config) -> List[files.File]:
    """
    Get images ready to be created.

    Args:
        config: the config.

    Returns:
        The images list.
    """
    ImageData = collections.namedtuple("ImageData", "path width height")
    images = []
    images_data: Tuple[ImageData, ...]

    if config.get("favicon_ico"):
        images.append(
            # favicon ico version, used for most browsers and opensearch
            files.File(
                path=config["output_folder_path"] / "favicon.ico",
                data=read_image_bytes(config["favicon_ico"]),
            )
        )

    if config.get("favicon_png"):
        images_data = (
            # favicon png version, used for most browsers
            ImageData(path=config["output_folder_path"] / "static" / "favicon-16x16.png", width=16, height=16),
            ImageData(path=config["output_folder_path"] / "static" / "favicon-32x32.png", width=32, height=32),
            ImageData(path=config["output_folder_path"] / "static" / "favicon-96x96.png", width=96, height=96),
            ImageData(path=config["output_folder_path"] / "static" / "favicon-192x192.png", width=192, height=192),
            ImageData(path=config["output_folder_path"] / "static" / "favicon-194x194.png", width=194, height=194),
            # apple icon
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-icon-57x57.png", width=57, height=57),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-icon-60x60.png", width=60, height=60),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-icon-72x72.png", width=72, height=72),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-icon-76x76.png", width=76, height=76),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-icon-114x114.png", width=114, height=114),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-icon-120x120.png", width=120, height=120),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-icon-128x128.png", width=128, height=128),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-icon-144x144.png", width=144, height=144),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-icon-152x152.png", width=152, height=152),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-icon-167x167.png", width=167, height=167),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-icon-180x180.png", width=180, height=180),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-icon-195x195.png", width=195, height=195),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-icon-196x196.png", width=196, height=196),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-icon-228x228.png", width=228, height=228),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-icon-512x512.png", width=512, height=512),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-icon-1024x1024.png", width=1024, height=1024),
            # browserconfig
            ImageData(path=config["output_folder_path"] / "static" / "browserconfig-30x30.png", width=30, height=30),
            ImageData(path=config["output_folder_path"] / "static" / "browserconfig-44x44.png", width=44, height=44),
            ImageData(path=config["output_folder_path"] / "static" / "browserconfig-70x70.png", width=70, height=70),
            ImageData(path=config["output_folder_path"] / "static" / "browserconfig-150x150.png", width=150, height=150),
            ImageData(path=config["output_folder_path"] / "static" / "browserconfig-310x150.png", width=310, height=150),
            ImageData(path=config["output_folder_path"] / "static" / "browserconfig-310x310.png", width=310, height=310),
            ImageData(path=config["output_folder_path"] / "static" / "browserconfig-144x144.png", width=144, height=144),
            # manifest
            ImageData(path=config["output_folder_path"] / "static" / "manifest-192x192.png", width=192, height=192),
            ImageData(path=config["output_folder_path"] / "static" / "manifest-512x512.png", width=512, height=512),
            # opensearch
            ImageData(path=config["output_folder_path"] / "static" / "opensearch-16x16.png", width=16, height=16),
            # apple startup image
            # Source: https://github.com/onderceylan/pwa-asset-generator
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-1024x1024.png", width=1024, height=1024),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-2048x2732.png", width=2048, height=2732),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-2732x2048.png", width=2732, height=2048),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-1668x2388.png", width=1668, height=2388),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-2388x1668.png", width=2388, height=1668),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-1668x2224.png", width=1668, height=2224),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-2224x1668.png", width=2224, height=1668),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-1536x2048.png", width=1536, height=2048),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-2048x1536.png", width=2048, height=1536),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-1242x2688.png", width=1242, height=2688),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-2688x1242.png", width=2688, height=1242),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-1125x2436.png", width=1125, height=2436),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-2436x1125.png", width=2436, height=1125),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-828x1792.png", width=828, height=1792),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-1792x828.png", width=1792, height=828),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-1242x2208.png", width=1242, height=2208),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-2208x1242.png", width=2208, height=1242),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-750x1334.png", width=750, height=1334),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-1334x750.png", width=1334, height=750),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-640x1136.png", width=640, height=1136),
            ImageData(path=config["output_folder_path"] / "static" / "apple-touch-startup-image-1136x640.png", width=1136, height=640),
        )
        images.extend(
            files.File(
                path=image.path,
                data=read_image_bytes(resize_image(image=config["favicon_png"], width=image.width, height=image.height)),
            )
            for image in images_data
        )

        # yandex
        image = ImageData(path=config["output_folder_path"] / "static" / "yandex.png", width=120, height=120)
        resized_image = resize_image(image=config["favicon_png"], width=image.width, height=image.height)
        if config.get("background_color") is not None:
            parsed_image = remove_transparency(image=resized_image, background_color=str(config["background_color"]))
        else:
            parsed_image = resized_image
        images.append(files.File(data=read_image_bytes(parsed_image), path=image.path))

    if config["favicon_svg"] is not None:
        images.append(
            files.File(
                path=config["output_folder_path"] / "static" / "mask-icon.svg",
                data=getattr(config["favicon_svg"], "read_bytes", bytes)(),
            )
        )

    if config.get("preview_png"):
        images_data = (
            # og
            ImageData(path=config["output_folder_path"] / "static" / "preview-600x600.png", width=600, height=600),
            ImageData(path=config["output_folder_path"] / "static" / "preview-1080x1080.png", width=1080, height=1080),
            # twitter
            ImageData(path=config["output_folder_path"] / "static" / "preview-600x600.png", width=600, height=600),
            # microdata
            ImageData(path=config["output_folder_path"] / "static" / "preview-600x600.png", width=600, height=600),
        )
        images.extend(
            files.File(
                path=image.path,
                data=read_image_bytes(resize_image(image=config["favicon_png"], width=image.width, height=image.height)),
            )
            for image in images_data
        )

    return images
