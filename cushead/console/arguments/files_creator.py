"""
Handle the files creation.
"""
from __future__ import annotations

import pathlib
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple

from cushead.console import logs
from cushead.generator import files


class Error(NamedTuple):
    """
    Store error data.
    """

    error: str
    path: pathlib.Path


class Node:
    """
    Represent a node.

    Can have child nodes and own data.
    """

    def __init__(self, *, name: str, data: Optional[bytes] = None) -> None:
        """
        Create a node.

        Args:
            name: the name.
            data: the data.
        """
        self.name = name
        self.data = data
        self.childrens: Dict[str, Node] = {}

    def add_child(self, *, parts: Tuple[str, ...], data: bytes) -> None:
        """
        Add children node.

        To add a child node, you must define its path within the current node. Each part of the path represents a node.
        The path is interpreted as follows: the first part represents a child node of the current node, the second part
        represents a child node of the first node.
        The last part is the node to be added, it is to which the defined data will be added. If any of the nodes in
        the path does not exist, it will be created.

        Args:
            parts: path of the child in the node.
            data: child data.
        """
        if len(parts) > 1:
            if parts[0] not in self.childrens:
                self.childrens[parts[0]] = Node(name=parts[0])
            self.childrens[parts[0]].add_child(parts=parts[1:], data=data)
        else:
            self.childrens[parts[0]] = Node(name=parts[0], data=data)


def create_node(*, node_items: List[files.File]) -> Node:
    """
    Create a node structure based on a list of files to create.

    Args:
        node_items: a list that have info about the files to create.

    Returns:
        A node tree.
    """
    base_path = Node(name="")
    for file in node_items:
        base_path.add_child(parts=pathlib.Path(file.path).parts, data=file.data)
    return base_path


def parse_node(*, node: Node, base_path: pathlib.Path) -> Tuple[bool, List[Error]]:
    """
    Create a representation of a node in the system directory.

    Args:
        node: the node.
        base_path: the base path where the files will be created.

    Returns:
        If at least one file has been created.
        Files with errors.
    """
    errors = []
    file_has_been_created = False

    for name, subnode in sorted(node.childrens.items()):
        destination_path = base_path / name

        # Create children node.
        if subnode.data:
            try:
                destination_path.write_bytes(subnode.data or bytes())
            except OSError as exception:
                errors.append(Error(error=str(exception.__class__.__name__), path=destination_path))
            else:
                file_has_been_created = True
                logs.show_created_file(path=destination_path)

        # Create parent node.
        else:
            if not destination_path.exists():
                destination_path.mkdir()
            sub_node_created_files, sub_node_errors = parse_node(node=subnode, base_path=destination_path)
            file_has_been_created = file_has_been_created or sub_node_created_files
            errors.extend(sub_node_errors)

    return file_has_been_created, errors


def create_files(*, files_to_create: List[files.File]) -> None:
    """
    Create files based on a list.

    Args:
        files_to_create: a list that have info about the elements to create inside the node.
    """
    node = create_node(node_items=files_to_create)

    print("Created files:")
    created_files, errors = parse_node(node=node, base_path=pathlib.Path(""))
    if not created_files:
        print(" * No one file has been created.")
    logs.show_created_file_errors(errors=errors)
