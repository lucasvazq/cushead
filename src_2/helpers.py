""" global variables """

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