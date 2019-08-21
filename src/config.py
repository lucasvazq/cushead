#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from json.decoder import JSONDecodeError
from os import path

from .helpers import Errors


class Config:
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
        jsonstring = None
        try:
            jsonstring = json.loads(filestring)
        except JSONDecodeError:
            e = (
                f"Invalid json file format in ({filename})\n"
                f"FILE PATH: {filepath}"
            )
            Errors.error_message(e)

        # Construct config
        recommended = jsonstring.get('recommended', {})
        default = jsonstring.get('default', {})
        general = default.get('general', {})
        basic = default.get('basic', {})
        social_media = default.get('social_media', {})
        progressive_web_app = jsonstring.get('progressive_web_apps', {})
        if 'required' not in jsonstring:
            e = "Miss 'required' object and it's required."
            Errors.error_message(e)
        jsonstring = {**jsonstring['required'], **recommended, **general,
                      **basic, **social_media, **progressive_web_app}
        self.config = jsonstring

        # Required values
        Errors.required_key(self.config, 'files_output')
        Errors.required_key(self.config, 'static_url')

        return jsonstring
