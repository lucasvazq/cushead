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

    # Sanitize static_url key
    # Prevent:
    #   output = /output/
    #   static_url = /static/
    #   output + static_url = /static/ [root/static/]
    if json_string['static_url'][0] == '/':
        json_string['static_folder_path'] = json_string['static_url'][1:]
    # HEre, prevent //
    if json_string['static_url'][-1] == '/':
        json_string['static_url'] = json_string['static_url'][:-1]

    # Make paths
    # Define the main path as the passed throught -file argument
    json_string['main_folder_path'] = path.dirname(args.file)
    json_string['output_folder_path'] = path.join(
        json_string['main_folder_path'],
        'output'
    )
    json_string['static_folder_path'] = path.join(
        json_string['output_folder_path'],
        json_string['static_folder_path']
    )
    return json_string
