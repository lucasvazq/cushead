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

    fullpath = path.join(os.getcwd(), args.file)
    with open(args.file, 'r') as fileinstance:
        filestring = fileinstance.read()
    jsonstring = None
    try:
        jsonstring = json.loads(filestring)
    except JSONDecodeError:
        exception = (
            f"Invalid json file format in ({args.file})\n"
            f"FILE PATH: {fullpath}"
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
    Errors.required_key(config, 'static_url')

    return jsonstring
