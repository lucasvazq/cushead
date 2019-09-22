#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Handle the generations of files"""

import json
import os
from os import path

from PIL import Image
from resizeimage import resizeimage

from .helpers import (error_message, FilesHelper, FilesValidator,
                      FoldersHelper, KeysValidator)


class Icons:
    def favicon_ico(self):
        """favicon.ico"""

        if not self._requirements('favicon_ico'):
            return []

        # Root destination
        source = path.join(self.config['main_path'],
                           self.config['favicon_ico'])
        destination = path.join(self.config['output_path'], "favicon.ico")
        FilesHelper.copy_file(source, destination)

    def favicon_svg(self):
        """favicon.svg"""

        if not self._requirements('favicon_svg'):
            return []

        source = path.join(self.config['main_path'],
                           self.config['favicon_svg'])
        destination = path.join(self.config['static_url_path'], "favicon.svg")
        FilesHelper.copy_file(source, destination)


    def preview_png(self):
        """preview.png"""

        if not self._requirements('preview_png'):
            return []

        source = path.join(self.config['main_path'],
                           self.config['preview_png'])
        destination = path.join(self.config['static_url_path'], "preview.png")
        FilesHelper.copy_file(source, destination)

    @staticmethod
    def resize(image, size, filepath):
        """Resize a image"""
        cover = resizeimage.resize_contain(image, [size[0], size[1]])
        cover.save(filepath, image.format)


class ComplementaryFiles(Icons):
    """Main class of this module"""
    config = {}


    def generate(self):
        """Generate HTML head elements and new files"""

        head = []

        # Favicon .png version
        # Multiples elements
        elements = self.favicon_png()
        head.extend(elements)

        # Favicon .ico version
        # Only one element
        element = self.favicon_ico()
        head.append(element)

        # Favicon .svg version
        # Only one element
        element = self.favicon_svg()
        head.append(element)

        # Preview .png
        # Multiples elements
        elements = self.preview_png()
        head.extend(elements)

        # browserconfig.xml
        browserconfig_content, browserconfig_head = self.browserconfig()
        head.append(browserconfig_head)
        filepath = path.join(self.config['static_url_path'],
                             'browserconfig.xml')
        FilesHelper.write_file(filepath, browserconfig_content)

        # manifest.json
        manifest_content, manifest_head = self.manifest()
        head.append(manifest_head)
        filepath = path.join(self.config['static_url_path'], 'manifest.json')
        FilesHelper.write_file(filepath, manifest_content)

        # opensearch.xml
        opensearch_content, opensearch_head = self.opensearch()
        head.append(opensearch_head)
        filepath = path.join(self.config['static_url_path'], 'opensearch.xml')
        FilesHelper.write_file(filepath, opensearch_content)

        if 'clean_url' in self.config:
            # robots.txt
            robots_content = self.robots()
            filepath = path.join(self.config['output_path'], 'robots.txt')
            FilesHelper.write_file(filepath, robots_content)

            # sitemap.xml
            sitemap_content = self.sitemap()
            filepath = path.join(self.config['output_path'], 'sitemap.xml')
            FilesHelper.write_file(filepath, sitemap_content)

        return head
