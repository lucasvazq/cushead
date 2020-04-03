#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src_2 import support
from src_2.generator import base_generator
from src_2.configuration import configuration


def generate_files(config):
    support.Support().check_for_execution()
    generator.BaseGenerator(config).generate_files()


def generate_default_config(output_path, add_assets=False):
    support.Support().check_for_execution()
    configuration.generate_default_config(output_path, add_assets)
