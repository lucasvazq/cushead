#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from typing import List
"""Module to handle the creation of no image related tags

Classes:
    General
"""


class General:
    """Generate general tags

    Methods:
        general
        basic
        complementary_files
        social_medi
    """

    config = {}
    image_format_config_dict = {}

    def general(self) -> List[str]:
        # DONE
        """Return a list of tags related to the general config of a website"""
        head = []
        # content-type
        string = self.config.get("content-type", "")
        head.append(f"<meta http-equiv='Content-Type' " f"content='{string}'>")
        # X-UA-Compatible
        string = self.config.get("X-UA-Compatible", "")
        head.append(f"<meta http-equiv='X-UA-Compatible' "
                    f"content='{string}'>")
        # viewport
        string = self.config.get("viewport", "")
        head.append(f"<meta name='viewport' content='{string}'>")
        # locale
        string = self.config.get("language", "")
        head.append(f"<meta http-equiv='Content-Language' "
                    f"content='{string}'>")
        # robots
        string = self.config.get("robots", "")
        head.append(f"<meta name='robots' content='{string}'>")
        # apple
        head.extend([
            "<meta name='apple-mobile-web-app-capable' content='yes'>",
            ("<meta name='apple-mobile-web-app-status-bar-style' "
             "content='black-translucent'>"),
        ])
        return head

    def basic(self) -> List[str]:
        # DONE
        """Return a list of tags related to a basic and standart seo"""
        head = []
        # title
        string = self.config.get("title", "")
        head.extend([
            f"<title>{string}</title>",
            f"<meta name='application-name' content='{string}'>",
            f"<meta name='apple-mobile-web-app-title' "
            f"content='{string}'>",
        ])
        # description
        string = self.config.get("description", "")
        head.append(f"<meta name='description' content='{string}'>")
        # subject
        string = self.config.get("subject", "")
        head.append(f"<meta name='subject' content='{string}'>")
        # keywords
        string = self.config.get("keywords", "")
        head.append(f"<meta name='keywords' content='{string}'>")
        # theme-color and msapplication-TileColor
        string = self.config.get("background_color", "")
        head.extend([
            f"<meta name='theme-color' content='{string}'>",
            f"<meta name='msapplication-TileColor' content='{string}'>",
        ])
        # author
        string = self.config.get("author", "")
        head.append(f"<meta name='author' content='{string}'>")
        return head

    def complementary_files(self) -> List[str]:
        # DONE
        """Return a list with tags related to complementary files"""
        static_url = self.config.get("static_url", "")
        title = self.config.get("title", "")
        return [
            # browserconfig.xml
            (f"<meta name='msapplication-config' "
             f"content='{static_url}/browserconfig.xml'>"),
            # manifest.json
            (f"<link rel='manifest' href='{static_url}"
             f"/manifest.json'>"),
            # opensearch.xml
            (f"<link rel='search' "
             f"type='application/opensearchdescription+xml' "
             f"title='{title}' href='{static_url}"
             f"/opensearch.xml'>"),
        ]

    def social_media(self) -> List[str]:
        # DONE
        """Return a list with tags related to social media"""
        head = []

        # OPENGRAPH AND FACEBOOK

        # fb:app_id
        string = self.config.get("facebook_app_id", "")
        head.append(f"<meta porperty='fb:app_id' content='{string}'>")
        # og:locale
        language = self.config.get("language", "")
        territory = ("_{}".format(self.config["territory"])
                     if "territory" in self.config else "")
        string = language + territory
        head.append(f"<meta property='og:locale' content='{string}'>")
        # og:type
        # Only allow website type for simplicity
        head.append("<meta property='og:type' content='website'>")
        # og:url, Likes and Shared are stored under this url
        string = self.config.get("protocol", "")
        string += self.config.get("clean_url", "")
        head.append(f"<meta property='og:url' content='{string}'>")
        # og:site_name
        string = self.config.get("title", "")
        head.append(f"<meta property='og:site_name' content='{string}'>")
        # og:title
        string = self.config.get("title", "")
        head.append(f"<meta property='og:title' content='{string}'>")
        # og:description
        string = self.config.get("description", "")
        head.append(f"<meta property='og:description' content='{string}'>")
        # og:image:type
        # Only allow png type for simplicity
        head.append("<meta property='og:image:type' content='image/png'>")
        # og:image:alt and twitter:image:alt
        title = self.config.get("title", "")
        description = self.config.get("description", "")
        connector = (" - " if "title" in self.config
                     and "description" in self.config else "")
        string = title + connector + description
        head.extend([
            f"<meta property='og:image:alt' content='{string}'>",
            f"<meta name='twitter:image:alt' content='{string}'>",
        ])

        # TWITTER
        # twitter:image mixed with op:image and op:image:secure in OPENGRAH
        # section
        # twitter:image:alt mixed with op:image:alt in OPENGRAPH section

        # twitter:card
        # Only allow summary type for simplicity
        head.append("<meta name='twitter:card' content='summary'>")
        # twitter:site
        string = self.config.get("twitter_user_@", "")
        head.append(f"<meta name='twitter:site' content='{string}'>")
        # twitter:title
        string = self.config.get("title", "")
        head.append(f"<meta name='twitter:title' content='{string}'>")
        # twitter:description
        string = self.config.get("description", "")
        head.append(f"<meta name='twitter:description' content='{string}'>")
        # tw:creator
        string = self.config.get("twitter_user_id", "")
        head.append(f"<meta property='twitter:creator:id' "
                    f"content='{string}'>")

        return head

    def json_ld(self) -> List[str]:
        # DONE
        protocol = self.config.get("protocol", "")
        clean_url = self.config.get("clean_url", "")
        static_url = self.config.get("static_url", "")
        description = self.config.get("description", "")
        website_url = f"{protocol}{clean_url}"
        json_ld_dict = {
            "@context": "http://schema.org/",
            "@type": "Organization",
            "@id": website_url,
            "url": website_url,
            "slogan": description,
            "description": description,
        }
        if static_url:
            if static_url[0] == "/":
                static_slash = ""
            else:
                static_slash = "/"
                static_url_full_path = (
                    f"{protocol}{clean_url}{static_slash}{static_url}")
            preview_png = self.image_format_config_dict.get(
                "preview_og")._output_formater()[0]
            json_ld_dict.update({
                "logo":
                f"{static_url_full_path}/{preview_png}",
                "image":
                f"{static_url_full_path}/{preview_png}",
            })
        return [
            f"<script type='application/ld+json'>{json.dumps(json_ld_dict)}</script>"
        ]
