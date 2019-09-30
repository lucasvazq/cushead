#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to handle the creation of the main index.html file

Classes:
    Base
"""

from os import path

from src.module.files.head.base import Head


class BaseFileCreation(Head):
    """Class to handle the creation of the main index.html file

    Methods:
        full_index() -> dict
        structure(head: list = []) -> str
    """

    def full_index(self) -> dict:
        """Create full index.html structure with head tag included

        Return
            dict: 1

        1)
            content str: file content
            destination_file_path str: path where the file must be  written
        """
        head = self.full_head()
        index = self.structure(head)
        destination_file_path = path.join(
            self.config.get('output_folder_path', ''),
            'index.html'
        )
        return {
            'index': {
                'content': index,
                'destination_file_path': destination_file_path,
            }
        }

    @staticmethod
    def structure(head: list = None or []) -> str:
        """Return an html structure

        Args:
            head list (default = []): tags elements that conform the head of an
                html structure

        """
        indent = "    "  # 4 spaces
        formated_head = ''.join([
            f"{indent*2}{tag}\n"
            for conjunt in head
            for tag in conjunt
        ])
        return (f"<html>\n"
                f"{indent}<head>\n"
                f"{formated_head}"  # Already have newline
                f"{indent}</head>\n"
                f"</html>").replace('\'', '"')
