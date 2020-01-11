#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to handle the creation of the main index.html file

Classes:
    BaseFileCreation
"""

from os import path
from typing import Dict, List, Union

from src.module.files.head.base import Head


class BaseFileCreation(Head):
    """Class to handle the creation of the main index.html file

    Methods:
        full_index
        structure
    """

    def full_index(self) -> Dict[str, Dict[str, str]]:
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

    def structure(self, list_head: Union[List[List[str]], None] = None) -> str:
        head = list_head or []
        """Return an html structure"""
        indent = "    "  # 4 spaces
        formated_head = ''.join([
            f"{indent*2}{tag}\n"
            for conjunt in head
            for tag in conjunt
        ])
        language = self.config.get('language', '')
        return (f"<html lang='{language}'>\n"
                f"{indent}<head>\n"
                f"{formated_head}"  # Already have newline
                f"{indent}</head>\n"
                f"<body></body>"
                f"</html>").replace('\'', '"')
