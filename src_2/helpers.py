""" global variables """

INDENTATION = " " * 4


def write_output(file_name, destionation_path, content):
    pass


def indent_dict(dictionary, base_indentation_level):
    indented_content = ",\n".join([f"{INDENTATION * (base_indentation_level + 1)}'{key}': '{value}'" for key, values in dictionary])}
    return (
        f"{INDENTATION * base_indentation_level}{{\n"
        f"{indented_content}\n"
        f"{INDENTATION * base_indentation_level}}}"
    )