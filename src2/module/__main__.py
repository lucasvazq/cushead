#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Arguments handler"""

import os
from os import path

from .files.complementary_files import ComplementaryFiles
from .files.base import Base
from .config import DefaultIconsConfig, ImagesCreationConfig
from ..console.arguments import parse_args
from ..helpers import FilesHelper, FoldersHelper
from ..info import get_info
from ..module.presets import Presets

class DefaultConfig(DefaultIconsConfig):
    pass

class Config(ImagesCreationConfig):
    pass

class Files(Base, ComplementaryFiles):
    def all_files(self):
        return dict(self.full_index(), **self.full_complementary_files())

class Main(Config, DefaultConfig, Files, Presets):
    def __init__(self, config=None, icons_config=None):
        self.config = config
        self.icons_config = icons_config or self.default_icons_config()
