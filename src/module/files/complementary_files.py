#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to handle the creation of files that aren't the index.html or images

Classes:
    ComplementaryFiles
"""

import json
from os import path


class ComplementaryFiles:
    config: dict
    icons_config: dict

    def _browserconfig(self) -> dict:
        """browserconfig.xml content
        Return the content of browserconfig.xml and the path where must be
        written

        Return
            dict: 1

        1)
            content str: file content
            destination_path str: path where the file must be written
        """
        browserconfig_config = self.icons_config.get('browserconfig', {})
        icon = browserconfig_config.get('filename', '')
        square_sizes = browserconfig_config.get('square_sizes', [])
        non_square_sizes = browserconfig_config.get('non_square_sizes', [])
        static_url = self.config.get('static_url', '')
        background_color = self.config.get('background_color', '')
        content = ("<?xml version='1.0' encoding='utf-8'?>"
                   "<browserconfig><msapplication><tile>")
        content += ''.join([
            "<square{0}x{0}logo src='{1}{2}-{0}x{0}.png' />".format(
                size,
                static_url,
                icon
            )
            for size in square_sizes
        ])
        content += ''.join([
            "<wide{0}x{1}logo src='{2}{3}-{0}x{1}.png' />".format(
                size[0],
                size[1],
                static_url,
                icon
            )
            for size in non_square_sizes
        ])
        content += (f"<TileColor>"
                    f"{background_color}"
                    f"</TileColor></tile></msapplication>"
                    f"</browserconfig>")
        content = content.replace('\'', '"')
        destination_path = path.join(
            self.config.get('static_folder_path', ''),
            'browserconfig.xml'
        )
        return {
            'content': content,
            'destination_path': destination_path,
        }

    def _manifest(self) -> dict:
        """manifest.json content
        Return the content of manifest.json and the path where must be written

        Return
            dict: 1

        1)
            content str: file content
            destination_path str: path where the file must be written
        """
        manifest_config = self.icons_config.get('manifest', {})
        content = dict()
        content['name'] = self.config.get('title', '')
        content['short_name'] = self.config.get('title', '')
        content['description'] = self.config.get('description', '')
        content['dir'] = self.config.get('dir', '')
        content['start_url'] = self.config.get('start_url', '')
        content['orientation'] = self.config.get('orientation', '')
        content['background_color'] = self.config.get('background_color', '')
        content['theme_color'] = self.config.get('background_color', '')
        content['default_locale'] = self.config.get('language', '')
        content['scope'] = self.config.get('scope', '')
        content['display'] = self.config.get('display', '')
        content['platform'] = self.config.get('platform', '')
        content['related_applications'] = self.config.get('applications', '')
        content['icons'] = [
            {
                'src': "{0}{1}-{2}x{2}".format(
                    self.config.get('static_url', ''),
                    manifest_config.get('filename', ''),
                    size
                ),
                'sizes': f"{size}x{size}",
                'type': 'image/png',
                'density': str(size / 48)
            }
            for size in manifest_config.get('square_sizes', [])
        ]
        content = json.dumps(content)
        destination_path = path.join(
            self.config.get('static_folder_path', ''),
            'manifest.json'
        )
        return {
            'content': content,
            'destination_path': destination_path,
        }

    def _opensearch(self) -> dict:
        """opensearch.xml content
        Return the content of opensearch.xml and the path where must be written

        Return
            dict: 1

        1)
            content str: file content
            destination_path str: path where the file must be written
        """
        static_url = self.config.get('static_url', '')
        title = self.config.get('title', '')
        url = self.config.get('url', '')
        content = ("<?xml version='1.0' encoding='utf-8'?>"
                   "<OpenSearchDescription xmlns:moz='"
                   "http://www.mozilla.org/2006/browser/search/' "
                   "xmlns='http://a9.com/-/spec/opensearch/1.1/'>"
                   "</OpenSearchDescription>"
                   "<ShortName>{0}</ShortName>"
                   "<Description>Search {0}</Description>"
                   "<InputEncoding>UTF-8</InputEncoding>"
                   "<Url method='get' type='text/html' "
                   "template='http://www.google.com/search?q="
                   "{{searchTerms}}+site%3A{1}' />"
                   "<Image height='16' width='16' type='image/png'>"
                   "{2}/opensearch-16x16.png"
                   "</Image>")
        content = content.format(title, url, static_url)
        content = content.replace('\'', '"')
        destination_path = path.join(
            self.config.get('static_folder_path', ''),
            'opensearch.xml'
        )
        return {
            'content': content,
            'destination_path': destination_path,
        }

    def _robots(self) -> dict:
        """robots.txt content
        Return the content of robots.txt and the path where must be written

        Return
            dict: 1

        1)
            content str: file content
            destination_path str: path where the file must be written
        """
        protocol = self.config.get('protocol', '')
        clean_url = self.config.get('clean_url', '')
        sitemap_reference = (
            "\n"
            f"Sitemap: {protocol}"
            f"{clean_url}/sitemap.xml"
            if 'sitemap' in self.config else ''
        )
        content = (f"User-agent: *\n"
                   f"Allow: /\n"
                   f"{sitemap_reference}")
        destination_path = path.join(
            self.config.get('output_folder_path', ''),
            'robots.txt'
        )
        return {
            'content': content,
            'destination_path': destination_path,
        }

    def _sitemap(self) -> dict:
        """sitemap.xml content
        Return the content of sitemap.xml and the path where must be
        written

        Return
            dict: 1

        1)
            content str: file content
            destination_path str: path where the file must be written
        """
        protocol = self.config.get('protocol', '')
        clean_url = self.config.get('clean_url', '')
        content = (f"<?xml version='1.0' encoding='uft-8'?>"
                   f"<urlset xmlns="
                   f"'http://www.sitemaps.org/schemas/sitemap/0.9' "
                   f"xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' "
                   f"xsi:schemaLocation="
                   f"'http://www.sitemaps.org/schemas/sitemap/0.9 "
                   f"http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'>"
                   f"<url><loc>{protocol}{clean_url}/</loc></url></urlset>")
        content = content.replace('\'', '"')
        destination_path = path.join(
            self.config.get('output_folder_path', ''),
            'sitemap.xml'
        )
        return {
            'content': content,
            'destination_path': destination_path,
        }

    def full_complementary_files(self) -> dict:
        """Return all complementary files structure with their path

        Return
            dict: 1

        1)
            Keys are browserconfig, manifest, opensearch, robots and sitemap.
            Each key has of value another dict that has the keys content and
            destination_path. They represent the content of each complementary
            file and the path where there must be written.
        """
        return {
            'browserconfig': self._browserconfig(),
            'manifest': self._manifest(),
            'opensearch': self._opensearch(),
            'robots': self._robots(),
            'sitemap': self._sitemap(),
        }
