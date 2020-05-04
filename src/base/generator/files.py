import hashlib
from os import path
from typing import Dict, List, NoReturn, TypedDict, Union

import jinja2

from src.base.generator import parser
from src.base.generator import images


from src.base import configuration
IconFamily = List[Dict[str, configuration.ImageFormater]]


class IconsConfig(TypedDict):
    favicon_ico: IconFamily
    favicon_png: IconFamily
    favicon_svg: IconFamily
    preview_png: IconFamily
    browserconfig: IconFamily
    manifest: IconFamily
    opensearch: IconFamily


class Config(TypedDict, total=False):
    main_folder_path: str
    output_folder_path: str
    static_folder_path: str
    static_url: str
    favicon_ico: str
    favicon_png: str
    favicon_svg: str
    preview_png: str
    google_tag_manager: str
    language: str
    territory: str
    domain: str
    dir: str
    title: str
    description: str
    subject: str
    main_color: str
    background_color: str
    author_name: str
    facebook_app_id: str
    twitter_username: str
    twitter_user_id: str
    itunes_app_id: str
    itunes_affiliate_data: str


class MiscData(TypedDict, total=False):
    hyp_lt: str
    us_lt: str
    itunes_app: str
    preview_image: str
    title_and_or_description: str


class TextFilesGenerator(images.Images):

    def __init__(self, *,
                 config: Config,
                 icons_config: IconsConfig,
                 indentation: str) -> NoReturn:
        self.config = config
        self.icons_config = icons_config
        self.indentation = indentation
        self.misc_data = self.setup_data()
        self.template_environment = self.setup_template_reader()
        self.misc_data['index_hash'] = self.generate_index_hash()

    def generate_index_hash(self) -> str:
        index_content = self.generate_index()["content"]
        index_hash = hashlib.sha1(index_content.encode('utf-8')).hexdigest()
        short_hash = index_hash[0:6]
        return short_hash

    def setup_data(self) -> MiscData:
        misc_data = {}
        language = self.config.get("language")
        territory = self.config.get("territory")
        itunes_app_id = self.config.get("itunes_app_id")
        itunes_affiliate_data = self.config.get("itunes_affiliate_data")
        og_image = self.icons_config.get('preview_og')
        twitter_image = self.icons_config.get('twitter_image')
        title = self.config.get("title")
        description = self.config.get("description")

        if language:
            if all((language, territory)):
                hyphen = "-"
                underscore = "_"
            else:
                hyphen = ""
                underscore = ""
            misc_data['hyp_lt'] = f'{language}{hyphen}{territory}'
            misc_data['us_lt'] = f'{language}{underscore}{territory}'

        if itunes_app_id:
            itunes_content = [f"app-id={itunes_app_id}"]
            if itunes_affiliate_data:
                itunes_content.append(f'affiliate-data={itunes_affiliate_data}')
            itunes_content.append('app-argument=/')
            misc_data['itunes_app'] = ', '.join(itunes_content)

        if "domain" in self.config and any((og_image, twitter_image)):
            preview_png_config = og_image or twitter_image
            image_name = preview_png_config._output_formater()[0].file_name
            misc_data['preview_image'] = image_name

        if any((og_image, twitter_image)) and any((title, description)):
            if all((title, description)):
                headline_conector = " - "
            else:
                headline_conector = ""
            headline = f"{title or ''}{headline_conector}{description or ''}"
            misc_data["title_and_or_description"] = headline

        return misc_data

    def setup_template_reader(self) -> jinja2.Environment:
        templates_folderpath = path.join(path.dirname(path.realpath(__file__)), 'templates')
        template_loader = jinja2.FileSystemLoader(searchpath=templates_folderpath)
        extensions = ['src.base.generator.jinja_extension.OneLineExtension']
        template_environment = jinja2.Environment(loader=template_loader, extensions=extensions)
        template_environment.globals.update({
            'config': self.config,
            'misc_data': self.misc_data,
            'icons_config': self.icons_config,
            'static_url': self.config['static_url'],
            'wse': "http://www.google.com",
            'gtm_url': "https://www.googletagmanager.com",
            'gf_url': "https://fonts.googleapis.com",
            'gf_family': "css2?family=Roboto:wght@400&display=swap",
            'gapis_url': "https://storage.googleapis.com",
            'cf_url': "https://cdnjs.cloudflare.com/ajax/libs",
        })
        return template_environment

    def render_template(self, file_name):
        return self.template_environment.get_template(file_name).render()

    def generate_index(self):
        rendered_template = self.render_template('index_template.html')
        initial_data = {
            'indentation': self.indentation,
            'one_line_tags': ('title',),
            'self_close_tags': ('meta', 'link'),
        }
        content = parser.CustomHTMLParser(**initial_data).parse_content(content=rendered_template)
        output_file_path = path.join(self.config["output_folder_path"], "index.html")
        return {
            "content": content,
            "destination_file_path": output_file_path,
        }

    def generate_browserconfig(self) -> Union[Dict[str, str], None]:
        if not self.icons_config['browserconfig'] and "main_color" not in self.config:
            return

        rendered_template = self.render_template('browserconfig_template.xml')
        initial_data = {
            'camel_case_tags': ('TileColor', 'TileImage'),
            'indentation': self.indentation,
            'one_line_tags': ('TileColor',),
            'self_close_tags': ('TileImage',),
            'regex_self_close_tags': (r'square\d*x\d*', r'wide\d*x\d*'),
        }
        content = parser.CustomXMLParser(**initial_data).parse_content(content=rendered_template)
        destination_file_path = path.join(self.config["static_folder_path"], "browserconfig.xml")
        return {
            "content": content,
            "destination_file_path": destination_file_path,
        }

    def generate_humans(self) -> Union[Dict[str, str], None]:

        if "author_name" not in self.config and "author_email" not in self.config:
            return

        rendered_template = self.render_template('humans_template.html')
        initial_data = {
            'indentation_trigger': '/*',
            'indentation': self.indentation,
        }
        content = parser.CustomPlainTextParser(**initial_data).parse_content(content=rendered_template)

        output_file_path = path.join(self.config["output_folder_path"], "humans.txt")
        return {
            "content": content,
            "destination_file_path": output_file_path,
        }

    def generate_manifest(self) -> Dict[str, str]:
        rendered_template = self.render_template('manifest_template.html')
        initial_data = {
            'indentation': self.indentation
        }
        content = parser.CustomScriptParser(**initial_data).parse_content(content=rendered_template)
        output_file_path = path.join(self.config["static_folder_path"], "manifest.json")
        return {
            "content": content,
            "destination_file_path": output_file_path,
        }

    def generate_opensearch(self) -> Dict[str, str]:
        rendered_template = self.render_template('opensearch_template.xml')
        initial_data = {
            'camel_case_tags': ('OpenSearchDescription', 'ShortName',
                                'Description', 'InputEncoding', 'Url',
                                'Image'),
            'indentation': self.indentation,
            'one_line_tags': ('ShortName', 'Description', 'InputEncoding',
                              'Image'),
            'self_close_tags': ('Url',),
        }
        content = parser.CustomXMLParser(**initial_data).parse_content(content=rendered_template)
        output_file_path = path.join(self.config["static_folder_path"], "opensearch.xml")
        return {
            "content": content,
            "destination_file_path": output_file_path,
        }

    def generate_robots(self) -> Dict[str, str]:
        rendered_template = self.render_template('robots_template.html')
        initial_data = {
            'indentation': self.indentation,
            'new_line_trigger': 'Sitemap',
        }
        content = parser.CustomPlainTextParser(**initial_data).parse_content(content=rendered_template)
        output_file_path = path.join(self.config["output_folder_path"], "robots.txt")
        return {
            "content": content,
            "destination_file_path": output_file_path,
        }

    def generate_security(self) -> Union[Dict[str, str], None]:
        if "author_email" not in self.config:
            return None

        rendered_template = self.render_template('security_template.html')
        initial_data = {
            'indentation': self.indentation,
        }
        content = parser.CustomPlainTextParser(**initial_data).parse_content(content=rendered_template)
        output_file_path = path.join(self.config["output_folder_path"], ".well-known/security.txt")
        return {
            "content": content,
            "destination_file_path": output_file_path,
        }

    def generate_service_worker(self):
        rendered_template = self.render_template('service_worker_template.js')
        initial_data = {
            'indentation': self.indentation,
            'new_line_trigger': '//',
        }
        content = parser.CustomScriptParser(**initial_data).parse_content(content=rendered_template)
        output_file_path = path.join(self.config["static_folder_path"], "sw.js")
        return {
            "content": content,
            "destination_file_path": output_file_path,
        }

    def generate_sitemap(self) -> Union[Dict[str, str], None]:

        if "domain" not in self.config:
            return None

        rendered_template = self.render_template('sitemap_template.xml')
        initial_data = {
            'indentation': self.indentation,
            'one_line_tags': ('loc',),
        }
        content = parser.CustomXMLParser(**initial_data).parse_content(content=rendered_template)
        output_file_path = path.join(self.config["output_folder_path"], "sitemap.xml")
        return {
            "content": content,
            "destination_file_path": output_file_path,
        }


class ImagesGenerator:
    def __init__(self, config, icons_config):
        self.config = config
        self.icons_config = icons_config

    def creation(self) -> Dict[str, Union[str, List[int]]]:
        files = []
        for icon in self.icons_config.values():
            for size_format in icon.formated:
                files.append({
                    "file_name": size_format.file_name,
                    "size": size_format.size,
                    "output_folder_path": icon.output_folder_path,
                    "source_file_path": icon.source_file_path,
                    "background_color": icon.background_color,
                })
        return files

    def get_icons_creation_config(
            self
    ) -> List[Dict[str, Union[str, List[int]]]]:
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
        icons_creation_config = [self.creation()]
        return [
            element for group in icons_creation_config for element in group
        ]


class FilesGenerator(TextFilesGenerator, ImagesGenerator):

    def __init__(self, *, config, icons_config, indentation):
        super().__init__(config=config,
                         icons_config=icons_config,
                         indentation=indentation)

    def generate(self):
        return {
            "text_files": self.generate_text_files(),
            "image_files": self.generate_media_files(),
        }

    def generate_text_files(self):
        generated_files = [
            self.generate_index(),
            self.generate_browserconfig(),
            self.generate_humans(),
            self.generate_manifest(),
            self.generate_opensearch(),
            self.generate_robots(),
            self.generate_security(),
            self.generate_service_worker(),
            self.generate_sitemap(),
        ]
        return filter(None, generated_files)

    def generate_media_files(self):
        return self.get_icons_creation_config()
