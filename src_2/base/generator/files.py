import os
import typing

import src_2.helpers
import src_2.base.generator.images


class IndexGenerator(src_2.base.generator.images.Images):

    def __init__(self, config, icons_config, image_format_config_dict):
        self.config = config
        self.icons_config = icons_config
        self.image_format_config_dict = image_format_config_dict

    def generate_index(self):
        return [{
            'content': self.index_base(),
            'destination_file_path': os.path.join(self.config.get("output_folder_path", ""), "index.html")
        }]

    def index_base(self):
        return (
            f"<html lang='{self.config['language']}'>\n"
            f"{self.index_head()}\n"
            f"{self.index_body()}\n"
            "</html>"
        ).replace("'", '"')

    def index_head(self):
        head = []

        # content-type
        head.append(f"<meta http-equiv='Content-Type' content='{self.config['content-type']}'>")
        # X-UA-Compatible
        head.append(f"<meta http-equiv='X-UA-Compatible' "
                    f"content='{self.config['X-UA-Compatible']}'>")
        # viewport
        head.append(f"<meta name='viewport' content='{self.config['viewport']}'>")
        # locale
        head.append(f"<meta http-equiv='Content-Language' "
                    f"content='{self.config['language']}'>")
        # robots
        head.append(f"<meta name='robots' content='{self.config['robots']}'>")
        # apple
        head.extend([
            "<meta name='apple-mobile-web-app-capable' content='yes'>",
            ("<meta name='apple-mobile-web-app-status-bar-style' "
             "content='black-translucent'>"),
        ])

        # title
        head.extend([
            f"<title>{self.config['title']}</title>",
            f"<meta name='application-name' content='{self.config['title']}'>",
            (
                "<meta name='apple-mobile-web-app-title' "
                f"content='{self.config['title']}'>"
            ),
        ])
        # description
        head.append(f"<meta name='description' content='{self.config['description']}'>")
        # subject
        head.append(f"<meta name='subject' content='{self.config['subject']}'>")
        # theme-color and msapplication-TileColor
        head.extend([
            f"<meta name='theme-color' content='{self.config['background_color']}'>",
            f"<meta name='msapplication-TileColor' content='{self.config['background_color']}'>",
        ])
        # author
        head.append(f"<meta name='author' content='{self.config['author']}'>")

        # images
        for image_type in self.icons_config.values():
            for brand in image_type:
                for sizes in brand.formated:
                    head_element = self.icons_head_creator(brand, sizes.file_name, sizes.size)
                    if head_element:
                        head.append(head_element)

        # browserconfig.xml
        head.append(f"<meta name='msapplication-config' content='{self.config['static_url']}/browserconfig.xml'>")
        # manifest.json
        head.append(f"<link rel='manifest' href='{self.config['static_url']}/manifest.json'>")
        # opensearch.xml
        head.append(
            f"<link rel='search' type='application/opensearchdescription+xml' title='{self.config['title']}' href='{self.config['static_url']}/opensearch.xml'>"
        )

        # fb:app_id
        head.append(f"<meta porperty='fb:app_id' content='{self.config['facebook_app_id']}'>")
        # og:locale
        head.append(f"<meta property='og:locale' content='{self.config['language']}_{self.config['territory']}'>")
        # og:type
        # Only allow website type for simplicity
        head.append("<meta property='og:type' content='website'>")
        # og:url, Likes and Shared are stored under this url
        string = self.config.get("protocol", "")
        string += self.config.get("clean_url", "")
        head.append(f"<meta property='og:url' content='{string}'>")
        # og:site_name
        head.append(f"<meta property='og:site_name' content='{self.config['title']}'>")
        # og:title
        head.append(f"<meta property='og:title' content='{self.config['title']}'>")
        # og:description
        head.append(f"<meta property='og:description' content='{self.config['description']}'>")
        # og:image:type
        # Only allow png type for simplicity
        head.append("<meta property='og:image:type' content='image/png'>")
        # og:image:alt
        head.append(f"<meta property='og:image:alt' content='{self.config['title']} - {self.config['description']}'>")

        # twitter:card
        # Only allow summary type for simplicity
        head.append("<meta name='twitter:card' content='summary'>")
        # twitter:site
        head.append(f"<meta name='twitter:site' content='{self.config['twitter_user_@']}'>")
        # twitter:title
        head.append(f"<meta name='twitter:title' content='{self.config['title']}'>")
        # twitter:description
        head.append(f"<meta name='twitter:description' content='{self.config['description']}'>")
        # tw:creator
        head.append(f"<meta property='twitter:creator:id' "
                    f"content='{self.config['twitter_user_id']}'>")
        # tw:image:alt
        head.append(f"<meta name='twitter:image:alt' content='{self.config['title']} - {self.config['description']}'>")

        image_name = self.image_format_config_dict["preview_og"]._output_formater()[0].file_name
        json_ld = src_2.helpers.indent_dict({
            '@context': 'http://schema.org/',
            '@type': 'Organization',
            '@id': f"{self.config['protocol']}{self.config['clean_url']}",
            'url': f"{self.config['protocol']}{self.config['clean_url']}",
            'slogan': f"{self.config['description']}",
            'description': f"{self.config['description']}",
            'logo': f"{self.config['protocol']}{self.config['clean_url']}/static/{image_name}",
            'image': f"{self.config['protocol']}{self.config['clean_url']}/static/{image_name}",
        }, 2)
        head.append(
            "<script type='application/ld+json'>\n"
            f"{json_ld}\n"
            f"{src_2.helpers.INDENTATION* 2 }</script>"
        )

        # convert to string adding indent
        head_content = f"{src_2.helpers.INDENTATION * 2}".join([f"{tag}\n" for tag in head])
        return (
            f"{src_2.helpers.INDENTATION}<head>\n"
            f"{src_2.helpers.INDENTATION * 2}{head_content}"
            f"{src_2.helpers.INDENTATION}</head>"
        ).replace("'", '"')

    def index_body(self):
        return f"{src_2.helpers.INDENTATION}<body></body>"


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
        browserconfig_config = self.icons_config["browserconfig"][0]
        icon_name = browserconfig_config.output_file_name
        sizes_square = browserconfig_config.sizes_square
        sizes_rectangular = browserconfig_config.sizes_rectangular
        content = ("<?xml version='1.0' encoding='utf-8'?>\n"
                   "<browserconfig>\n"
                   f"{src_2.helpers.INDENTATION}<msapplication>\n"
                   f"{src_2.helpers.INDENTATION * 2}<tile>\n")
        content += "".join([
            (
                f"{src_2.helpers.INDENTATION * 3}"
                f"<square{size}x{size}logo "
                f"src='{self.config['static_url']}/{icon_name}-{size}x{size}.png'/>\n"
            )
            for size in sizes_square
        ])
        content += "".join([
            (
                f"{src_2.helpers.INDENTATION * 3}"
                f"<wide{size[0]}x{size[1]}logo "
                f"src='{self.config['static_url']}/{icon_name}-{size[0]}x{size[1]}.png'/>\n"
            )
            for size in sizes_rectangular
        ])
        content += f"{src_2.helpers.INDENTATION * 3}<TileColor>{self.config['background_color']}</TileColor>\n"
        content += (
            f"{src_2.helpers.INDENTATION * 2}</tile>\n"
            f"{src_2.helpers.INDENTATION}</msapplication>\n"
            "</browserconfig>"
        )
        destination_file_path = os.path.join(self.config.get("static_folder_path", ""), "browserconfig.xml")
        return {
            "content": content.replace("'", '"'),
            "destination_file_path": destination_file_path,
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
        manifest_config = self.icons_config["manifest"][0]
        content = dict()
        content["name"] = self.config["title"]
        content["short_name"] = self.config["title"]
        content["description"] = self.config["description"]
        content["dir"] = self.config["dir"]
        content["start_url"] = self.config["start_url"]
        content["orientation"] = self.config["orientation"]
        content["background_color"] = self.config["background_color"]
        content["theme_color"] = self.config["background_color"]
        content["default_locale"] = self.config["language"]
        content["scope"] = self.config["scope"]
        content["display"] = self.config["display"]
        content["platform"] = self.config["platform"]
        content["icons"] = [
            {
                "src":
                f"{self.config['static_url']}/{manifest_config.output_file_name}-{size}x{size}",
                "sizes":
                f"{size}x{size}",
                "type": "image/png",
                "density":
                str(size / 48),
            }
            for size in manifest_config.sizes_square
        ]
        destination_file_path = os.path.join(self.config.get("static_folder_path", ""), "manifest.json")
        return {
            "content": src_2.helpers.indent_dict(content, 0).replace("'", '"'),
            "destination_file_path": destination_file_path,
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
        opensearch_config = self.icons_config["opensearch"][0]
        size = opensearch_config.sizes_square[0]
        # crear una lista en vez de este string "content"
        content = (f"<?xml version='1.0' encoding='utf-8'?>\n"
                   f"<OpenSearchDescription xmlns:moz='"
                   f"http://www.mozilla.org/2006/browser/search/' "
                   f"xmlns='http://a9.com/-/spec/opensearch/1.1/'>\n"
                   f"{src_2.helpers.INDENTATION}<ShortName>{self.config['title']}</ShortName>\n"
                   f"{src_2.helpers.INDENTATION}<Description>Search {self.config['title']}</Description>\n"
                   f"{src_2.helpers.INDENTATION}<InputEncoding>UTF-8</InputEncoding>\n"
                   f"{src_2.helpers.INDENTATION}<Url method='get' type='text/html' "
                   f"template='http://www.google.com/search?q="
                   f"{{searchTerms}}+site%3A{self.config['clean_url']}'/>\n"
                   f"{src_2.helpers.INDENTATION}<Image height='{size}' width='{size}' "
                   f"type='{opensearch_config.attribute_type}'>"
                   f"{self.config['static_url']}/{opensearch_config.output_file_name}-16x16.png"  # Output file name doesnt give already the sizes?
                   f"</Image>\n"
                   f"</OpenSearchDescription>")
        destination_file_path = os.path.join(self.config.get("static_folder_path", ""), "opensearch.xml")
        return {
            "content": content.replace("'", '"'),
            "destination_file_path": destination_file_path,
        }

    def robots_content(self) -> typing.Dict[str, str]:
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
        content = (f"User-agent: *\n"
                   f"Allow: /\n"
                   f"\n"
                   f"Sitemap: {protocol}{clean_url}/sitemap.xml")
        destination_file_path = os.path.join(self.config.get("output_folder_path", ""), "robots.txt")
        return {
            "content": content,
            "destination_file_path": destination_file_path,
        }

    def sitemap_content(self) -> typing.Dict[str, str]:
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
        content = (f"<?xml version='1.0' encoding='utf-8'?>"
                   f"<urlset xmlns="
                   f"'http://www.sitemaps.org/schemas/sitemap/0.9' "
                   f"xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' "
                   f"xsi:schemaLocation="
                   f"'http://www.sitemaps.org/schemas/sitemap/0.9 "
                   f"http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'>"
                   f"<url><loc>{protocol}{clean_url}/</loc></url>"
                   f"</urlset>")
        content = content.replace("'", '"')
        destination_file_path = os.path.join(
            self.config.get("output_folder_path", ""), "sitemap.xml")
        return {
            "content": content,
            "destination_file_path": destination_file_path,
        }

    def generate_complementary_files(self):
        return [
            self.complementary_browserconfig(),
            self.complementary_manifest(),
            self.complementary_opensearch(),
            self.robots_content(),
            self.sitemap_content(),
        ]


class ImagesGenerator:

    def __init__(self, config, icons_config):
        self.config = config
        self.icons_config = icons_config

    def _creation(self) -> typing.Dict[str, typing.Union[str, typing.List[int]]]:
        files = []
        for image_type in self.icons_config.values():
            for brand in image_type:
                for size_format in brand.formated:
                    files.append({
                        'file_name': size_format.file_name,
                        'size': size_format.size,
                        'output_folder_path': brand.output_folder_path,
                        'source_file_path': brand.source_file_path,
                    })
        return files

    def get_icons_creation_config(self) \
            -> typing.List[typing.Dict[str, typing.Union[str, typing.List[int]]]]:
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
        icons_creation_config = [
            self._creation()
        ]
        return [
            element for group in icons_creation_config
            for element in group
        ]


class FilesGenerator(IndexGenerator, ComplementaryFilesGenerator, ImagesGenerator):

    def generate_non_media_files(self):
        return self.generate_index() + self.generate_complementary_files()

    def generate_media_files(self):
        return self.get_icons_creation_config()
