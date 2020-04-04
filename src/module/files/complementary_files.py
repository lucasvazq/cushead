#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to handle the creation of files that aren't the index.html or images

Classes:
    ComplementaryFilesCreation
"""
import json
from os import path
from typing import Dict


class ComplementaryFilesCreation:
    # DONE
    """Class to generate complementary files tags

    Methods:
        full_complementary_files
        browserconfig_content
        manifest_content
        opensearch_content
        robots_content
        sitemap_content
    """

    config = {}
    icons_config = {}

    def full_complementary_files(self) -> Dict[str, Dict[str, str]]:
        """Return all complementary files structure with their path

        Return
            dict: 1

        1)
            Keys are browserconfig, manifest, opensearch, robots and sitemap.
            Each key has of value another dict that has the keys content and
            destination_file_path. They represent the content of each
            complementary file and the path where there must be written.
        """
        return {
            "browserconfig": self.browserconfig_content(),
            "manifest": self.manifest_content(),
            "opensearch": self.opensearch_content(),
            "robots": self.robots_content(),
            "sitemap": self.sitemap_content(),
        }

    def browserconfig_content(self) -> Dict[str, str]:
        """browserconfig.xml content
        Return the content of browserconfig.xml and the path where must be
        written

        Return
            dict: 1

        1)
            content str: file content
            destination_file_path str: path where the file must be written
        """
        browserconfig_config = self.icons_config.get("browserconfig", [])
        if browserconfig_config:
            browserconfig_config = browserconfig_config[0]
        icon = getattr(browserconfig_config, "output_file_name", "")
        sizes_square = getattr(browserconfig_config, "sizes_square", [])
        sizes_rectangular = getattr(
            browserconfig_config, "sizes_rectangular", []
        )
        static_url = self.config.get("static_url", "")
        background_color = self.config.get("background_color", "")
        content = (
            "<?xml version='1.0' encoding='utf-8'?>"
            "<browserconfig>"
            "<msapplication>"
            "<tile>"
        )
        content += "".join(
            [
                "<square{0}x{0}logo src='{1}/{2}-{0}x{0}.png'/>".format(
                    size, static_url, icon
                )
                for size in sizes_square
            ]
        )
        content += "".join(
            [
                "<wide{0}x{1}logo src='{2}/{3}-{0}x{1}.png'/>".format(
                    size[0], size[1], static_url, icon
                )
                for size in sizes_rectangular
            ]
        )
        content += (
            f"<TileColor>{background_color}</TileColor>"
            f"</tile>"
            f"</msapplication>"
            f"</browserconfig>"
        )
        content = content.replace("'", '"')
        destination_file_path = path.join(
            self.config.get("static_folder_path", ""), "browserconfig.xml"
        )
        return {
            "content": content,
            "destination_file_path": destination_file_path,
        }

    def manifest_content(self) -> Dict[str, str]:
        """manifest.json content
        Return the content of manifest.json and the path where must be written

        Return
            dict: 1

        1)
            content str: file content
            destination_file_path str: path where the file must be written
        """
        manifest_config = self.icons_config.get("manifest", [])[0]
        content = dict()
        content["name"] = self.config.get("title", "")
        content["short_name"] = self.config.get("title", "")
        content["description"] = self.config.get("description", "")
        content["dir"] = self.config.get("dir", "")
        content["start_url"] = self.config.get("start_url", "")
        content["orientation"] = self.config.get("orientation", "")
        content["background_color"] = self.config.get("background_color", "")
        content["theme_color"] = self.config.get("background_color", "")
        content["default_locale"] = self.config.get("language", "")
        content["scope"] = self.config.get("scope", "")
        content["display"] = self.config.get("display", "")
        content["platform"] = self.config.get("platform", "")
        content["icons"] = [
            {
                "src": "{0}/{1}-{2}x{2}".format(
                    self.config.get("static_url", ""),
                    getattr(manifest_config, "output_file_name", ""),
                    size,
                ),
                "sizes": f"{size}x{size}",
                "type": "image/png",
                "density": str(size / 48),
            }
            for size in getattr(manifest_config, "sizes_square", [])
        ]
        content = json.dumps(content)
        destination_file_path = path.join(
            self.config.get("static_folder_path", ""), "manifest.json"
        )
        return {
            "content": content,
            "destination_file_path": destination_file_path,
        }

    def opensearch_content(self) -> Dict[str, str]:
        """opensearch.xml content
        Return the content of opensearch.xml and the path where must be written

        Return
            dict: 1

        1)
            content str: file content
            destination_file_path str: path where the file must be written
        """
        opensearch_config = self.icons_config.get("opensearch", [])[0]
        file_name = getattr(opensearch_config, "output_file_name", "")
        size = getattr(opensearch_config, "sizes_square", [0])[0]
        file_type = getattr(opensearch_config, "attribute_type", "")
        static_url = self.config.get("static_url", "")
        title = self.config.get("title", "")
        url = self.config.get("clean_url", "")
        content = (
            f"<?xml version='1.0' encoding='utf-8'?>"
            f"<OpenSearchDescription xmlns:moz='"
            f"http://www.mozilla.org/2006/browser/search/' "
            f"xmlns='http://a9.com/-/spec/opensearch/1.1/'>"
            f"<ShortName>{title}</ShortName>"
            f"<Description>Search {title}</Description>"
            f"<InputEncoding>UTF-8</InputEncoding>"
            f"<Url method='get' type='text/html' "
            f"template='http://www.google.com/search?q="
            f"{{searchTerms}}+site%3A{url}'/>"
            f"<Image height='{size}' width='{size}' "
            f"type='{file_type}'>"
            f"{static_url}/{file_name}-16x16.png"
            f"</Image>"
            f"</OpenSearchDescription>"
        )
        content = content.replace("'", '"')
        destination_file_path = path.join(
            self.config.get("static_folder_path", ""), "opensearch.xml"
        )
        return {
            "content": content,
            "destination_file_path": destination_file_path,
        }

    def robots_content(self) -> Dict[str, str]:
        """robots.txt content
        Return the content of robots.txt and the path where must be written

        Return
            dict: 1

        1)
            content str: file content
            destination_file_path str: path where the file must be written
        """
        protocol = self.config.get("protocol", "")
        clean_url = self.config.get("clean_url", "")
        content = (
            f"User-agent: *\n"
            f"Allow: /\n"
            f"\n"
            f"Sitemap: {protocol}{clean_url}/sitemap.xml"
        )
        destination_file_path = path.join(
            self.config.get("output_folder_path", ""), "robots.txt"
        )
        return {
            "content": content,
            "destination_file_path": destination_file_path,
        }

    def sitemap_content(self) -> Dict[str, str]:
        """sitemap.xml content
        Return the content of sitemap.xml and the path where must be
        written

        Return
            dict: 1

        1)
            content str: file content
            destination_file_path str: path where the file must be written
        """
        protocol = self.config.get("protocol", "")
        clean_url = self.config.get("clean_url", "")
        content = (
            f"<?xml version='1.0' encoding='utf-8'?>"
            f"<urlset xmlns="
            f"'http://www.sitemaps.org/schemas/sitemap/0.9' "
            f"xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' "
            f"xsi:schemaLocation="
            f"'http://www.sitemaps.org/schemas/sitemap/0.9 "
            f"http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'>"
            f"<url><loc>{protocol}{clean_url}/</loc></url>"
            f"</urlset>"
        )
        content = content.replace("'", '"')
        destination_file_path = path.join(
            self.config.get("output_folder_path", ""), "sitemap.xml"
        )
        return {
            "content": content,
            "destination_file_path": destination_file_path,
        }
