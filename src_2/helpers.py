""" global variables """
import os
import shutil
import typing

import resizeimage
import PIL


INDENTATION = " " * 4


def write_output(file_name, destination_path, content):
    pass


def indent_dict(dictionary, base_indentation_level):
    """
    indented_content = []
    for key, value in dictionary:
        indented_content.append(
            f"{INDENTATION * (base_indentation_level + 1)}'{key}': '{value}'"
        )
    indented_content = ",\n".join(indented_content)
    """
    #indented_content = ",\n".join([f"{INDENTATION * (base_indentation_level + 1)}'{key}': '{value}'" for key, value in dictionary])}

    indented_content = []
    for key, value in dictionary:
        indentation = INDENTATION * (base_indentation_level + 1)
        indented_content.append(
            f"{indentation}'{key}': '{value}'"
        )
    indented_content = ",\n".join(indented_content)

    return (
        f"{INDENTATION * base_indentation_level}{{\n"
        f"{indented_content}\n"
        f"{INDENTATION * base_indentation_level}}}"
    )


# IMPROVE THIS, make it dynamic
def images_list() -> typing.List[str]:
    """Returns a list of image file names that are in assets"""
    return [
        'favicon_ico_16px.ico',
        'favicon_png_1600px.png',
        'favicon_svg_scalable.svg',
        'preview_png_500px.png',
    ]


def string_list_union(string_list: typing.Union[typing.List[str], None] = None) -> str:
    """Return a str list joined into a sentence

    Example:
        input = ['foo', 'bar', 'baz', 'etc']
        output = 'foo, bar, baz and etc'
    """
    string_list = string_list or []
    return ''.join([
        string + (
            ", " if string in string_list[:-2] else (
                " and " if string == string_list[-2] else ''
            )
        ) for string in string_list
    ])


def path_exists(file_path: str = '', key: str = ''):
    """Check if path exists"""
    full_path = os.path.join(os.getcwd(), file_path)
    if not os.path.exists(file_path):
        return (
            f"'{key}' ({file_path}) must be referred to a path "
            f"that exists.\n"
            f"PATH: {full_path}"
        )


def path_is_not_directory(file_path: str = '', key: str = ''):
    full_path = os.path.join(os.getcwd(), file_path)
    if not os.path.isfile(file_path):
        return (
            f"'{key}' key ({file_path}) must be referred to a "
            f"file path.\n"
            f"FILE PATH: {full_path}"
        )


def create_folder(destination_file_path):
    """Create folder"""
    if folder_path := os.path.dirname(destination_file_path):
        os.makedirs(folder_path, exist_ok=True)


def write_binary_file(binary_content, destination_file_path):
    """Write binary file"""
    create_folder(destination_file_path)
    with open(destination_file_path, 'wb') as file_instance:
        file_instance.write(binary_content)


def write_unicode_file(unicode_content, destination_file_path):
    """Write unicode file"""
    create_folder(destination_file_path)
    with open(destination_file_path, 'w') as file_instance:
        file_instance.write(unicode_content)


def format_sizes(icon_brand_config):
    sizes_square = getattr(icon_brand_config, 'sizes_square', [])
    sizes_square = [[size, size] for size in sizes_square]
    sizes_rectangular = getattr(icon_brand_config, 'sizes_rectangular', [])
    max_min_sizes = getattr(icon_brand_config, 'sizes_max_min', [])
    max_min_sizes = [[size[1], size[1]] for size in max_min_sizes]
    return sizes_square + sizes_rectangular + max_min_sizes


def copy_file(source_file_path, destination_file_path):
    """Copy file"""
    create_folder(destination_file_path)
    shutil.copyfile(source_file_path, destination_file_path)


def move_svg(destination_file_path, source_file_path):
    copy_file(source_file_path, destination_file_path)


def resize_image(destination_file_path, source_file_path, size):
    with open(source_file_path, 'rb') as file_instance, \
            PIL.Image.open(file_instance) as image_instance:
        cover = resizeimage.resizeimage.resize_contain(image_instance, [size[0], size[1]])
        cover.save(destination_file_path, image_instance.format)


def key_exists(key, dictionary):
    """Check if a key is in a dictionary"""
    if key not in dictionary:
        return f"Miss '{key}' key and it's required in config file."
