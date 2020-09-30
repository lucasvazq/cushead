#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc
"""
from __future__ import annotations

import pathlib
from typing import NoReturn


class DirNode:
    """
    doc
    """

    def __init__(self, name):
        self.elements = {}
        self.name = name

    def add_child(self, parts, data):
        """
        doc
        """

        if parts[1:]:
            if parts[0] not in self.elements:
                self.elements[parts[0]] = DirNode(parts[0])
            self.elements[parts[0]].add_child(parts[1:], data)
        else:
            self.elements[parts[0]] = FileNode(parts[0], data)


class FileNode:
    """
    doc
    """

    def __init__(self, name, data):
        self.name = name
        self.data = data


def get_files_tree(*, files_to_create: DirNode) -> DirNode:
    """
    doc
    """
    base_path = DirNode(name='')
    for file in files_to_create:
        base_path.add_child(parts=pathlib.Path(file.path).parts, data=file.data)
    return base_path


def parse_files_tree(*, files_tree: DirNode, base_path: pathlib.Path) -> NoReturn:
    """
    doc
    """
    for name, element in sorted(files_tree.elements.items()):
        destination_path = base_path / name
        if isinstance(element, FileNode):
            print(destination_path)
            destination_path.write_bytes(element.data)
        else:
            if not destination_path.exists():
                destination_path.mkdir()
            parse_files_tree(files_tree=element, base_path=destination_path)


def create_files(*, files_to_create) -> NoReturn:
    """
    doc
    """
    parse_files_tree(
        files_tree=get_files_tree(files_to_create=files_to_create),
        base_path=pathlib.Path(''),
    )
