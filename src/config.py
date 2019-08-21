#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys
import textwrap
from json.decoder import JSONDecodeError
from os import path

from .helpers import Helpers


class Config(Helpers):
    args = None
    config = None

    def __init__(self):
        super().__init__()

    def get_values(self):
        filename = self.args.file
        filepath = path.join(os.getcwd(), filename)
        f = open(filepath, 'r')
        filestring = f.read()
        f.close()
        try:
            jsonstring = json.loads(filestring)
        except JSONDecodeError:
            e = (
                f"Invalid json file format in ({filename})\n"
                f"FILE PATH: {filepath}"
            )
            self.error_message(e)

        # Construct config
        recommended = jsonstring.get('recommended', {})
        default = jsonstring.get('default', {})
        general = default.get('general', {})
        basic = default.get('basic', {})
        social_media = default.get('social_media', {})
        progressive_web_app = jsonstring.get('progressive_web_app', {})
        if 'required' not in jsonstring:
            e = "Miss 'required' object and it's required."
            self.error_message(e)
        jsonstring = {**jsonstring['required'], **recommended, **general,
                      **basic, **social_media, **progressive_web_app}
        self.config = jsonstring

        # Validate config
        self.validator()

        return jsonstring

    def validator(self):

        # Test: test_miss_output
        # Action: get in
        if 'files_output' not in self.config:
            self.error_message("Miss 'files_output' key and it's required.")

        output_filepath = path.join(os.getcwd(), self.config['files_output'])

        # Test: test_output_doesnt_exists
        # Action: get in
        if not path.exists(self.config['files_output']):
            e = (
                f"'files_output' ({self.config['files_output']}) must be "
                "referred to a folder path that exists."
                f"FOLDER PATH: {output_filepath}"
            )
            self.error_message(e)

        # Test: test_output_no_folder
        # Action: get in
        if not path.isdir(self.config['files_output']):
            e = (
                f"'files_output' ({self.config['files_output']}) must be "
                "referred to a folder path."
                f"FOLDER PATH: {output_filepath}"
            )
            self.error_message(e)

        # Test: test_miss_static_url
        # Action: get in
        if 'static_url' not in self.config:
            self.error_message("Miss 'static_url' key and it's required.")
