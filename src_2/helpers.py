""" global variables """
import typing

INDENTATION = " " * 4


def write_output(file_name, destionation_path, content):
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
images_list() -> typing.List[str]:
    """Returns a list of image file names that are in assets"""
    return [
        'favicon_ico_16px.ico',
        'favicon_png_1600px.png',
        'favicon_svg_scalable.svg',
        'preview_png_500px.png',
    ]


def string_list_union(string_list: typing.Union[List[str], None] = None) -> str:
    """Return a str list joined into a sentence

    Example:
        input = ['foo', 'bar', 'baz', 'etc']
        output = 'foo, bar, baz and etc'
    """
    string_list = string_list or []
    return ''.join([
        string + (
            ", " if string in self.string_list[:-2] else (
                " and " if string == self.string_list[-2] else ''
            )
        ) for string in self.string_list
    ])


def path_is_not_directory(file_path: str = '', key: str = ''):
    full_path = path.join(os.getcwd(), self.file_path)
    if not path.isfile(self.file_path):
        return (
            f"'{self.key}' key ({self.file_path}) must be referred to a "
            f"file path.\n"
            f"FILE PATH: {self.full_path}"
        )
