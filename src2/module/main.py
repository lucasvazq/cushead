#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Arguments handler"""

import os
from os import path

from .files.complementary_files import ComplementaryFiles
from .files.base import Base
from .config import DefaultIconsConfig
from ..console.arguments import parse_args
from ..helpers import FilesHelper, FoldersHelper
from ..info import get_info
from ..module.presets import Presets


class Files(Base, ComplementaryFiles):
    pass


class Main(Files, DefaultIconsConfig, Presets):
    def __init__(self, icons_config=None):
        self.icons_config = icons_config or self.default_icons_config()
