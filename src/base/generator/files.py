import hashlib
import json
import os
import textwrap
import typing

import src.base.generator.images
import src.helpers


class IndexGenerator(src.base.generator.images.Images):
    def __init__(self, config, icons_config, image_format_config_dict):
        self.config = config
        self.icons_config = icons_config
        self.image_format_config_dict = image_format_config_dict
        self.INDENTED_QUOTE = "$#@"

    def generate_index(self):
        return [{
            "content":
            self.index_base(),
            "destination_file_path":
            os.path.join(self.config["output_folder_path"], "index.html"),
        }]

    def index_base(self):

        html_tag_elements = ["<html class='no-js'"]
        # python 3.8
        # if (lang_data := self.config.get('language'), self.config.get('territory', ''))[0]:
        lang_data = (
            self.config.get("language"),
            self.config.get("territory", ""),
        )
        if lang_data[0]:
            conector = "-" if all(lang_data) else ""
            html_tag_elements.append(
                f"lang='{lang_data[0]}{conector}{lang_data[1]}'")
        if "dir" in self.config:
            html_tag_elements.append(f"dir='{self.config['dir']}'")
        html_tag = " ".join(html_tag_elements) + ">"

        return (f"\n".join([
            html_tag,
            f"{src.helpers.INDENTATION}{self.index_head()}",
            f"{src.helpers.INDENTATION}{self.index_body()}",
            "</html>",
        ]).replace("'", '"').replace(self.INDENTED_QUOTE, "'"))

    def index_head(self):
        favicons, og_social_media_images, twitter_social_media_images, late_browser_config = (
            self.generate_head_images())
        site_data = (
            self.config.get("title", ""),
            self.config.get("description", ""),
        )
        if (
            (og_social_media_images or twitter_social_media_images) and
            any(site_data)
        ):
            site_data_content = f"{site_data[0]}{' - ' if all(site_data) else ''}{site_data[1]}"
        else:
            site_data_content = ""

        # Order matters

        # Early browser configuration
        head = [
            "<meta charset='utf-8'>",
            "<!--[if IE]>",
            f"{src.helpers.INDENTATION}<meta http-equiv='X-UA-Compatible' content='ie=edge'>",
            "<![endif]-->",
            "<meta name='viewport' content='width=device-width,minimum-scale=1,initial-scale=1'>",
            "<meta name='apple-mobile-web-app-status-bar-style' content='black-translucent'>",
        ]
        if "background_color" in self.config:
            head.append(
                f"<meta name='theme-color' content='{self.config['background_color']}'>"
            )
        if "title" in self.config:
            head.append(f"<title>{self.config['title']}</title>")
        head.extend([
            "<meta name='apple-mobile-web-app-capable' content='yes'>",
            "<meta name='mobile-web-app-capable' content='yes'>",
        ])

        # Favicons
        head.extend(favicons)

        # Social media
        # python 3.8
        # if (lang_data := self.config.get('language'), self.config.get('territory', ''))[0]:
        lang_data = (
            self.config.get("language"),
            self.config.get("territory", ""),
        )
        if lang_data[0]:
            conector = "_" if all(lang_data) else ""
            head.append(
                f"<meta property='og:locale' content='{lang_data[0]}{conector}{lang_data[1]}'>"
            )
        head.append("<meta property='og:type' content='website'>")
        if "domain" in self.config:
            head.append(
                f"<meta property='og:url' content='https://{self.config['domain']}'>"
            )
        if "title" in self.config:
            head.extend([
                f"<meta property='og:site_name' content='{self.config['title']}'>",
                f"<meta property='og:title' content='{self.config['title']}'>",
            ])
        if "description" in self.config:
            head.append(
                f"<meta property='og:description' content='{self.config['description']}'>"
            )
        if og_social_media_images:
            head.extend([
                f"<meta property='og:image:alt' content='{site_data_content}'>",
                *og_social_media_images,
                "<meta property='og:image:type' content='image/png'>",
                "<meta propery='og:image:width' content='500'>",
                "<meta propery='og:image:height' content='500'>",
            ])
        head.append("<meta name='twitter:card' content='summary'>")
        if "twitter_user_@" in self.config:
            head.append(
                f"<meta name='twitter:site' content='{self.config['twitter_user_@']}'>"
            )
        if "twitter_user_id" in self.config:
            head.append(
                f"<meta name='twitter:site:id' content='{self.config['twitter_user_id']}'>"
            )
        if "title" in self.config:
            head.append(
                f"<meta name='twitter:title' content='{self.config['title']}'>"
            )
        if "description" in self.config:
            head.append(
                f"<meta name='twitter:description' content='{self.config['description']}'>"
            )
        if twitter_social_media_images:
            head.extend([
                f"<meta name='twitter:image:alt' content='{site_data_content}'>",
                *twitter_social_media_images,
            ])
        if "twitter_user_@" in self.config:
            head.append(
                f"<meta name='twitter:creator' content='{self.config['twitter_user_@']}'>"
            )
        if "twitter_user_id" in self.config:
            head.append(
                f"<meta property='twitter:creator:id' content='{self.config['twitter_user_id']}'>"
            )
        if "facebook_app_id" in self.config:
            head.append(
                f"<meta porperty='fb:app_id' content='{self.config['facebook_app_id']}'>"
            )
        # python 3.8
        # if (itunes_data := self.config.get('itunes_app_id'), self.config.get('itunes_affiliate_data'))[0]:
        itunes_data = (
            self.config.get("itunes_app_id"),
            self.config.get("itunes_affiliate_data"),
        )
        if itunes_data[0]:
            head.append(
                f"<meta name='apple-itunes-app' "
                f"content='app-id={itunes_data[0]}"
                f"{', ' if itunes_data[1] else ''}"
                f"affiliate-data={itunes_data[1] if itunes_data[1] else ''}"
                f", app-argument=/'>")

        # Fonts
        head.extend([
            (f"<link rel='preload' "
             f"href='https://fonts.googleapis.com/css2?family="
             f"Roboto:wght@400&display=swap' as='style' "
             f"onload='this.onload=null;this.rel="
             f"{self.INDENTED_QUOTE}stylesheet{self.INDENTED_QUOTE}'>"),
            "<noscript>",
            (f"{src.helpers.INDENTATION}<link "
             f"href='https://fonts.googleapis.com/css2?family="
             f"Roboto:wght@400&display=swap' rel='stylesheet'>"),
            "</noscript>",
        ])

        # Styles
        head.extend([
            "<style>",
            f"{src.helpers.INDENTATION}/* Add here your custom styles */",
            "</style>",
        ])

        # Early js
        head.extend([
            "<script>",
            f"{src.helpers.INDENTATION}// Add here your early load javascript",
            "</script>",
        ])

        # Late config
        head.append(
            f"<link rel='manifest' href='{self.config['static_url']}/manifest.json'>"
        )
        if "title" in self.config:
            head.extend([
                f"<meta name='application-name' content='{self.config['title']}'>",
                f"<meta name='apple-mobile-web-app-title' content='{self.config['title']}'>",
            ])
        if "background_color" in self.config:
            head.extend([
                f"<meta name='msapplication-TileColor' content='{self.config['background_color']}'>",
            ])
        if late_browser_config:
            head.extend(late_browser_config)
        if "title" in self.config:
            head.append(
                f"<link rel='search' type='application/opensearchdescription+xml' title='{self.config['title']}' href='{self.config['static_url']}/opensearch.xml'>"
            )
        head.extend([
            f"<meta name='robots' content='index, follow'>",
            f"<meta name='msapplication-config' content='{self.config['static_url']}/browserconfig.xml'>",
            "<meta name='referrer' content='origin-when-crossorigin'>",
            "<meta name='google-site-verification' content=''><!-- FILL THIS -->",
            "<meta name='baidu-site-verification' content=''><!-- FILL THIS -->",
        ])
        if "description" in self.config:
            head.append(
                f"<meta name='description' content='{self.config['description']}'>"
            )
        if "subject" in self.config:
            head.append(
                f"<meta name='subject' content='{self.config['subject']}'>")
        head.append(
            f"<meta name='author' content='{self.config['static_url']}/humans.txt'>"
        )

        # Structured data
        head.extend([
            "<script type='application/ld+json'>",
            f"{src.helpers.INDENTATION}{{",
            f"{src.helpers.INDENTATION * 2}'@context': 'http://schema.org/'",
            f"{src.helpers.INDENTATION * 2}'@type': 'Organization'",
        ])
        if "domain" in self.config:
            head.extend([
                f"{src.helpers.INDENTATION * 2}'@id': 'https://{self.config['domain']}'",
                f"{src.helpers.INDENTATION * 2}'url': 'https://{self.config['domain']}'",
            ])
        if "description" in self.config:
            head.extend([
                f"{src.helpers.INDENTATION * 2}'slogan': 'https://{self.config['description']}'",
                f"{src.helpers.INDENTATION * 2}'description': 'https://{self.config['description']}'",
            ])
        if "domain" in self.config and self.icons_config["preview_png"]:
            image_name = (self.icons_config["preview_png"]
                          [0]._output_formater()[0].file_name)
            head.extend([
                f"{src.helpers.INDENTATION * 2}'logo': '{self.config['domain']}{self.config['static_url']}/{image_name}'",
                f"{src.helpers.INDENTATION * 2}'image': '{self.config['domain']}{self.config['static_url']}/{image_name}'",
            ])
        head.extend([f"{src.helpers.INDENTATION}}}", "</script>"])

        # convert to string and add indent
        head_content = f"\n{src.helpers.INDENTATION * 2}".join(
            [tag for tag in head])
        return f"\n{src.helpers.INDENTATION}".join([
            f"<head>", f"{src.helpers.INDENTATION}{head_content}", f"</head>"
        ]).replace("'", '"')

    def index_body(self):
        body = [
            "<script src='https://cdnjs.cloudflare.com/ajax/libs/modernizr/2.8.3/modernizr.min.js'></script>",
            "<script>",
            f"{src.helpers.INDENTATION}if ('serviceWorker' in navigator && !navigator.serviceWorker.controller)",
            f"{src.helpers.INDENTATION * 2}navigator.serviceWorker.register('{self.config['static_url']}/sw.js', {{scope: '/'}});",
            "</script>",
        ]

        # convert to string and add indent
        body_content = f"\n{src.helpers.INDENTATION * 2}".join(
            [tag for tag in body])
        return f"\n{src.helpers.INDENTATION}".join([
            f"<body>", f"{src.helpers.INDENTATION}{body_content}", f"</body>"
        ]).replace("'", '"')


class ComplementaryFilesGenerator:
    def __init__(self, config, icons_config):
        self.config = config
        self.icons_config = icons_config

    def complementary_browserconfig(self) -> typing.Dict[str, str]:
        """browserconfig.xml content
        Return the content of browserconfig.xml and the path where must be
        written

        Return
            dict: 1

        1)
            content str: file content
            destination_file_path str: path where the file must be written
        """

        content = [
            "<browserconfig>",
            "<msapplication>",
            f"{src.helpers.INDENTATION}<tile>",
        ]

        if self.icons_config["browserconfig"]:
            browserconfig_config = self.icons_config["browserconfig"][0]
            icon_name = browserconfig_config.output_file_name
            sizes_square = browserconfig_config.sizes_square
            sizes_rectangular = browserconfig_config.sizes_rectangular
            content.extend([
                *[(f"{src.helpers.INDENTATION * 2}"
                   f"<square{size}x{size}logo "
                   f"src='{self.config['static_url']}/{icon_name}-{size}x{size}.png'/>"
                   ) for size in sizes_square],
                *[(f"{src.helpers.INDENTATION * 2}"
                   f"<wide{size[0]}x{size[1]}logo "
                   f"src='{self.config['static_url']}/{icon_name}-{size[0]}x{size[1]}.png'/>"
                   ) for size in sizes_rectangular],
            ])

        if "main_color" in self.config:
            content.append(
                f"{src.helpers.INDENTATION * 2}<TileColor>{self.config['main_color']}</TileColor>"
            )

        content.extend(
            [f"{src.helpers.INDENTATION}</tile>", "</msapplication>"])

        return {
            "content": ("<?xml version='1.0' encoding='utf-8'?>\n" +
                        f"\n{src.helpers.INDENTATION}".join(content) +
                        "\n</browserconfig>").replace("'", '"'),
            "destination_file_path":
            os.path.join(self.config["static_folder_path"],
                         "browserconfig.xml"),
        }

    def complementary_humans(self) -> typing.Dict[str, str]:
        content = []

        # python3.8
        # if any(author_data := (self.config.get("author_name"), self.config.get("author_email"))):
        author_data = (
            self.config.get("author_name"),
            self.config.get("author_email"),
        )
        if any(author_data):
            content.append("/* TEAM */")
            if author_data[0]:
                content.append(
                    f"{src.helpers.INDENTATION}Web designer: {author_data[0]}")
            if author_data[1]:
                content.append(
                    f"{src.helpers.INDENTATION}Contact: mailto:{author_data[1]}"
                )
            content.append("")

        content.extend(
            ["/* SITE */", f"{src.helpers.INDENTATION}Last update: *"])

        # python 3.8
        # if (lang_data := self.config.get('language'), self.config.get('territory', ''))[0]:
        lang_data = (
            self.config.get("language"),
            self.config.get("territory", ""),
        )
        if lang_data[0]:
            conector = "-" if all(lang_data) else ""
            content.append(
                f"{src.helpers.INDENTATION}Language: {lang_data[0]}{conector}{lang_data[1]}"
            )

        content.append(f"{src.helpers.INDENTATION}Doctype: HTML5")

        return {
            "content":
            "\n".join(content).replace("'", '"'),
            "destination_file_path":
            os.path.join(self.config["static_folder_path"], "humans.txt"),
        }

    def complementary_manifest(self) -> typing.Dict[str, str]:
        """manifest.json content
        Return the content of manifest.json and the path where must be written

        Return
            dict: 1

        1)
            content str: file content
            destination_file_path str: path where the file must be written
        """
        content = {}
        if "title" in self.config:
            content["name"] = self.config["title"]
            content["short_name"] = self.config["title"]
        if "description" in self.config:
            content["description"] = self.config["description"]
        if "dir" in self.config:
            content["dir"] = self.config["dir"]
        if "background_color" in self.config:
            content["background_color"] = self.config["background_color"]
            content["theme_color"] = self.config["background_color"]
        if "language" in self.config:
            content["default_locale"] = self.config["language"]
        content["start_url"] = "/"
        content["orientation"] = "landscape"
        content["scope"] = "/"
        content["display"] = "standalone"
        content["platform"] = "web"
        content["prefer_related_applications"] = False

        if self.icons_config["manifest"]:
            manifest_config = self.icons_config["manifest"][0]
            content["icons"] = [{
                "src":
                f"{self.config['static_url']}/{manifest_config.output_file_name}-{size}x{size}",
                "sizes": f"{size}x{size}",
                "type": "image/png",
                "purpose": "maskable any",
            } for size in manifest_config.sizes_square]

        return {
            "content":
            json.dumps(content, indent=src.helpers.INDENTATION),
            "destination_file_path":
            os.path.join(self.config["static_folder_path"], "manifest.json"),
        }

    def complementary_opensearch(self) -> typing.Dict[str, str]:
        """opensearch.xml content
        Return the content of opensearch.xml and the path where must be written

        Return
            dict: 1

        1)
            content str: file content
            destination_file_path str: path where the file must be written
        """
        content = [(f"<OpenSearchDescription xmlns:moz='"
                    f"http://www.mozilla.org/2006/browser/search/' "
                    f"xmlns='http://a9.com/-/spec/opensearch/1.1/'>")]

        if "title" in self.config:
            content.extend([
                f"<ShortName>{self.config['title']}</ShortName>",
                f"<Description>Search {self.config['title']}</Description>",
            ])

        content.append("<InputEncoding>UTF-8</InputEncoding>")

        if "domain" in self.config:
            content.append(
                "<Url method='get' type='text/html' "
                "template='http://www.google.com/search?q="
                f"{{searchTerms}}+site%3A{self.config['domain']}'/>")

        if self.icons_config["opensearch"]:
            opensearch_config = self.icons_config["opensearch"][0]
            size = opensearch_config.sizes_square[0]
            content.append(
                f"<Image height='{size}' width='{size}' "
                f"type='{opensearch_config.attribute_type}'>"
                f"{self.config['static_url']}/{opensearch_config.output_file_name}-16x16.png"
                f"</Image>")

        return {
            "content": ("<?xml version='1.0' encoding='utf-8'?>\n" +
                        f"\n{src.helpers.INDENTATION}".join(content) +
                        "\n</OpenSearchDescription>").replace("'", '"'),
            "destination_file_path":
            os.path.join(self.config["static_folder_path"], "opensearch.xml"),
        }

    def complementary_robots(self) -> typing.Dict[str, str]:
        """robots.txt content
        Return the content of robots.txt and the path where must be written

        Return
            dict: 1

        1)
            content str: file content
            destination_file_path str: path where the file must be written
        """
        content = [f"User-agent: *", f"Allow: /"]

        if "domain" in self.config:
            content.extend(
                [f"", f"Sitemap: https://{self.config['domain']}/sitemap.xml"])

        return {
            "content":
            "\n".join(content),
            "destination_file_path":
            os.path.join(self.config["output_folder_path"], "robots.txt"),
        }

    def complementary_security(self
                               ) -> typing.Union[typing.Dict[str, str], None]:

        if "author_email" not in self.config:
            return None

        content = [
            "# Our security address",
            f"Contact: {self.config['author_email']}",
        ]
        return {
            "content":
            "\n".join(content).replace("'", '"'),
            "destination_file_path":
            os.path.join(self.config["output_folder_path"],
                         ".well-known/humans.txt"),
        }

    def complementary_service_worker(self):
        content = textwrap.dedent(f"""\
            importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');
            const {{CacheFirst, StaleWhileRevalidate}} = workbox.strategies;
            const {{CacheableResponse}} = workbox.cacheableResponse;
            const {{registerRoute}} = workbox.routing;
            const {{ExpirationPlugin}} = workbox.expiration
            const {{precacheAndRoute}} = workbox.precaching
            const {{CacheableResponsePlugin}} = workbox.cacheableResponse

            workbox.setConfig({{
              skipWaiting: true,
              clientsClaim: true
            }});

            // Cache not very dynamic images
            registerRoute(
              /\.(?:png|gif|jpg|jpeg|webp|svg|ico)$/,
              new CacheFirst({{
                cacheName: 'images',
                plugins: [
                  new ExpirationPlugin({{
                    maxEntries: 60,
                    maxAgeSeconds: 30 * 24 * 60 * 60 // one month
                  }})
                ]
              }})
            );

            // Cache Google Fonts stylesheets
            registerRoute(
              /^https:\/\/fonts\.googleapis\.com/,
              new StaleWhileRevalidate({{
                cacheName: 'google-fonts-stylesheets',
              }})
            );

            // Cache Google Fonts webfont files
            registerRoute(
              /^https:\/\/fonts\.gstatic\.com/,
              new CacheFirst({{
                cacheName: 'google-fonts-webfonts',
                plugins: [
                  new CacheableResponsePlugin({{
                    statuses: [0, 200],
                  }}),
                  new ExpirationPlugin({{
                    maxAgeSeconds: 60 * 60 * 24 * 365 // one year
                  }})
                ]
              }})
            );

            // Cache js and css
            registerRoute(/\.(?:js|css)$/, new StaleWhileRevalidate());

            // Cache urls
            precacheAndRoute([
              {{url: "/index.html", revision: "{hashlib.sha1(self.generate_index()[0]["content"].encode('utf-8')).hexdigest()[0:6]}"}}
            ], {{
              cleanUrls: true
            }});
        """)
        return {
            "content":
            content,
            "destination_file_path":
            os.path.join(self.config["output_folder_path"], "sw.js"),
        }

    def complementary_sitemap(self
                              ) -> typing.Union[typing.Dict[str, str], None]:
        """sitemap.xml content
        Return the content of sitemap.xml and the path where must be
        written

        Return
            dict: 1

        1)
            content str: file content
            destination_file_path str: path where the file must be written
        """
        # If domain isn't defined, robots.txt cant refferer to sitemap
        if "domain" not in self.config:
            return None

        content = [
            "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>",
            "<url>",
            f"{src.helpers.INDENTATION}<loc>https://{self.config['domain']}/</loc>",
            "</url>",
        ]
        return {
            "content": ("<?xml version='1.0' encoding='utf-8'?>\n" +
                        f"\n{src.helpers.INDENTATION}".join(content) +
                        "\n</urlset>").replace("'", '"'),
            "destination_file_path":
            os.path.join(self.config["output_folder_path"], "sitemap.xml"),
        }

    def generate_complementary_files(self):
        return [
            file for file in [
                self.complementary_browserconfig(),
                self.complementary_humans(),
                self.complementary_manifest(),
                self.complementary_opensearch(),
                self.complementary_robots(),
                self.complementary_security(),
                self.complementary_service_worker(),
                self.complementary_sitemap(),
            ] if file
        ]


class ImagesGenerator:
    def __init__(self, config, icons_config):
        self.config = config
        self.icons_config = icons_config

    def _creation(self
                  ) -> typing.Dict[str, typing.Union[str, typing.List[int]]]:
        files = []
        for image_type in self.icons_config.values():
            for brand in image_type:
                for size_format in brand.formated:
                    files.append({
                        "file_name": size_format.file_name,
                        "size": size_format.size,
                        "output_folder_path": brand.output_folder_path,
                        "source_file_path": brand.source_file_path,
                        "background_color": brand.background_color,
                    })
        return files

    def get_icons_creation_config(
            self
    ) -> typing.List[typing.Dict[str, typing.Union[str, typing.List[int]]]]:
        """Return a list with default images creation configuration

        It's include configurations for the images listed in the assets folder

        Default structure of the dicts in the return is:
        {
            'destination_file_path': str,
            'resize': bool,
            'size': list,
            'source_file_path': str,
        }
        """
        icons_creation_config = [self._creation()]
        return [
            element for group in icons_creation_config for element in group
        ]


class FilesGenerator(IndexGenerator, ComplementaryFilesGenerator,
                     ImagesGenerator):
    def generate_non_media_files(self):
        return self.generate_index() + self.generate_complementary_files()

    def generate_media_files(self):
        return self.get_icons_creation_config()
