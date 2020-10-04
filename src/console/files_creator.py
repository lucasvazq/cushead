"""
Module used to create files.
"""
from __future__ import annotations

import pathlib
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from src.generator import files


class Node:
    """
    Class used to represent a parent node.
    """

    def __init__(self, name: str, data: Optional[bytes] = None) -> None:
        """
        Create a parent node.

        Args:
            name: the node name.
            data: the node data.
        """
        self.name = name
        self.data = data
        self.elements: Dict[str, Union[Node]] = {}

    def add_child(self, parts: Tuple[str, ...], data: bytes) -> None:
        """
        Add a child to node.

        Args:
            parts: path of the child in the node.
            data: child data.
        """
        if len(parts) > 1:
            if parts[0] not in self.elements:
                self.elements[parts[0]] = Node(parts[0])
            self.elements[parts[0]].add_child(parts[1:], data)
        else:
            self.elements[parts[0]] = Node(parts[0], data)


def create_node(*, node_items: List[files.File]) -> Node:
    """
    Create node based on a list.

    Args:
        node_items: a list that have info about the elements to create inside the node.

    Returns:
        A main dir node.
    """
    base_path = Node(name='')
    for file in node_items:
        base_path.add_child(parts=pathlib.Path(file.path).parts, data=file.data)
    return base_path


def parse_node(*, node: Node, base_path: pathlib.Path) -> None:
    """
    Create a representation of the node in the system directory.

    Args:
        node: the node.
        base_path: the base path.
    """
    for name, element in sorted(node.elements.items()):
        destination_path = base_path / name
        if element.data is not None:
            print(destination_path)
            destination_path.write_bytes(element.data)
        else:
            if not destination_path.exists():
                destination_path.mkdir()
            parse_node(node=element, base_path=destination_path)


def create_files(*, files_to_create: List[files.File]) -> None:
    """
    Create files based on a list.

    Args:
        files_to_create: a list that have info about the elements to create inside the node.
    """
    node = create_node(node_items=files_to_create)
    parse_node(node=node, base_path=pathlib.Path(''))
