#!/usr/bin/env python
# -*- coding: utf-8 -*-
import src.base.configuration
import src.base.generator.base_generator
import src.support


def generate_files(config):
    src.support.Support().check_for_execution()
    src.base.generator.base_generator.BaseGenerator(config).generate_files()


def generate_default_config(output_path, add_assets=False):
    src.support.Support().check_for_execution()
    src.base.configuration.generate_default_config(output_path, add_assets)
