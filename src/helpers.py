""" global variables """
import os
import shutil
import typing

import PIL.Image
import resizeimage.resizeimage

INDENTATION = " " * 2


def add_indent(element,
               base: int = 0,
               base_string: str = "",
               conector: str = ""):
    new_items = []
    if isinstance(element, list):
        for value in element:
            new_items.append(
                add_indent(
                    value,
                    base + 1,
                    base_string,
                    "" if value == element[-1] else ",",
                ))
    elif isinstance(element, dict):
        new_items.append(f"{INDENTATION * base}{{\n")
        nested_indentation = INDENTATION * (base + 1)
        for key, value in element.items():
            nested_conector = "" if key == list(element.keys())[-1] else ","
            if isinstance(value, dict):
                new_items.append(
                    f'{nested_indentation}"{key}": {{\n{add_indent(value, base + 1, base_string)}{nested_indentation}}}{nested_conector}\n'
                )
            elif isinstance(value, list):
                new_items.append(
                    f'{nested_indentation}"{key}": [\n{add_indent(value, base + 1, base_string)}{nested_indentation}]{nested_conector}\n'
                )
            else:
                new_items.append(
                    f'{nested_indentation}"{key}": "{value}"{nested_conector}\n'
                )
        new_items.append(f"{INDENTATION * base}}}{conector}\n")
    else:
        new_items.append(f'{INDENTATION * base}"{element}"{conector}\n')
    return base_string + "".join(new_items)





def path_exists(file_path: str = "", key: str = ""):
    """Check if path exists"""
    full_path = os.path.join(os.getcwd(), file_path)
    if not os.path.exists(file_path):
        return (f"'{key}' ({file_path}) must be referred to a path "
                f"that exists.\n"
                f"PATH: {full_path}")




def create_folder(destination_file_path):
    """Create folder"""
    # :=
    folder_path = os.path.dirname(destination_file_path)
    if folder_path:
        os.makedirs(folder_path, exist_ok=True)


def write_binary_file(binary_content, destination_file_path):
    """Write binary file"""
    create_folder(destination_file_path)
    with open(destination_file_path, "wb") as file_instance:
        file_instance.write(binary_content)


def write_unicode_file(unicode_content, destination_file_path):
    """Write unicode file"""
    create_folder(destination_file_path)
    with open(destination_file_path, "w") as file_instance:
        file_instance.write(unicode_content)


def copy_file(source_file_path, destination_file_path):
    """Copy file"""
    create_folder(destination_file_path)
    shutil.copyfile(source_file_path, destination_file_path)


def resize_image(source_file_path,
                 destination_file_path,
                 size,
                 background_color=None):
    with open(source_file_path, "rb") as file_instance, PIL.Image.open(
            file_instance) as image_instance:

        resized_image = resizeimage.resizeimage.resize_contain(
            image_instance, size)

        # Convert only transparent images (https://stackoverflow.com/a/35859141/10712525)
        if background_color and (resized_image.mode in ("RGBA", "LA") or
                                 (resized_image.mode == "P"
                                  and "transparency" in resized_image.info)):
            alpha = resized_image.convert("RGBA").getchannel("A")
            new_image = PIL.Image.new(
                "RGBA",
                resized_image.size,
                PIL.ImageColor.getrgb(background_color) + (255, ),
            )
            new_image.paste(resized_image, mask=alpha)
            image_to_save = new_image
        else:
            image_to_save = resized_image

        image_to_save.save(destination_file_path, resized_image.format)


def key_exists(key, dictionary):
    """Check if a key is in a dictionary"""
    if key not in dictionary:
        return f"Miss '{key}' key and it's required in config file."
















import pathlib
from typing import Iterable, Tuple, NamedTuple
import textwrap


class Image(NamedTuple):
    reference: str
    name: str
    data: bytes

def get_images_list() -> Tuple[Image]:
    """Returns a list of image file names that are in assets"""
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
    """Return a iterable represented into a sentence

    Example:
        input = ["foo", "bar", "baz", "etc"]
        output = "foo, bar, baz and etc"
    """
    return " and ".join(", ".join(string_list).rsplit(", ", 1))


def path_is_not_directory(
    *,
    key: str,
    file_path: str,
) -> str:
    """doc"""
    if not pathlib.Path(file_path).is_file():
        full_path = pathlib.Path(pathlib.Path.cwd(), file_path)
        return textwrap.dedent(f"""\
            '{key}' key ({file_path}) must be referred to a file path.
            REFERRED: {full_path}
        """)
