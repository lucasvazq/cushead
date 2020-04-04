#!/usr/bin/env python
# -*- coding: utf-8 -*-

import src_2.support
import src_2.base.generator.base_generator
import src_2.base.configuration


def generate_files(config):
    src_2.support.Support().check_for_execution()
    src_2.base.generator.base_generator.BaseGenerator(config).generate_files()


def generate_default_config(output_path, add_assets=False):
    src_2.support.Support().check_for_execution()
    src_2.base.configuration.generate_default_config(output_path, add_assets)
