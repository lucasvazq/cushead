#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Used for obtain config values"""

import json
from json.decoder import JSONDecodeError
import os
from os import path

from src2.helpers import error_message, KeysValidator


def get_values(args):
    """Read and obtain values as settings from json file"""
    
    with open(args.file, 'r') as file_instance:
        file_string = file_instance.read()
    json_string = None
    try:
        json_string = json.loads(file_string)
    except JSONDecodeError:
        config_file_fullpath = path.join(os.getcwd(), args.file)
        exception = (
            f"Invalid json file format in ({args.file})\n"
            f"FILE PATH: {config_file_fullpath}"
        )
        error_message(exception)

    # Construct config
    recommended = json_string.get('recommended', {})
    default = json_string.get('default', {})
    general = default.get('general', {})
    basic = default.get('basic', {})
    social_media = default.get('social_media', {})
    progressive_web_app = json_string.get('progressive_web_apps', {})
    if 'required' not in json_string:
        error_message("Miss 'required' object and it's required in config "
                      "file.")
    json_string = {**json_string['required'], **recommended, **general,
                  **basic, **social_media, **progressive_web_app}
    
    # Required values
    required_values = ['static_url']
    for key in required_values:
        KeysValidator(key, dictionary=json_string)

    # Add '/' to static url
    if json_string['static_url'][-1] != '/':
        json_string['static_url'] += '/'

    return json_string
