#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Used for obtain config values"""

import json
from json.decoder import JSONDecodeError
import os
from os import path

from .helpers import Errors


def get_values(args):
    """Read and obtain values as settings from json file"""

    filename = args.file
    filepath = path.join(os.getcwd(), filename)
    with open(filepath, 'r') as fileinstance:
        filestring = fileinstance.read()
    jsonstring = None
    try:
        jsonstring = json.loads(filestring)
    except JSONDecodeError:
        exception = (
            f"Invalid json file format in ({filename})\n"
            f"FILE PATH: {filepath}"
        )
        Errors.error_message(exception)

    # Construct config
    recommended = jsonstring.get('recommended', {})
    default = jsonstring.get('default', {})
    general = default.get('general', {})
    basic = default.get('basic', {})
    social_media = default.get('social_media', {})
    progressive_web_app = jsonstring.get('progressive_web_apps', {})
    if 'required' not in jsonstring:
        Errors.error_message("Miss 'required' object and it's required.")
    jsonstring = {**jsonstring['required'], **recommended, **general,
                  **basic, **social_media, **progressive_web_app}
    config = jsonstring

    # Required values
    Errors.required_key(config, 'files_output')
    Errors.required_key(config, 'static_url')

    return jsonstring
