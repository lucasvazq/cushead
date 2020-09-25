from __future__ import annotations


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





from typing import Union, List
import pathlib
from typing import NamedTuple

class Image(NamedTuple):
    reference: str
    name: str
    data: bytes

from typing import Optional

class File2(NamedTuple):
    """
    doc
    """
    path: str
    data: bytes


import PIL
import resizeimage
def resize_image(*,
        image: str,
        width: int,
        height: int,
    ):
        return resizeimage.resizeimage.resize_contain(image, (width, height))

def remove_transparency(*, image, background_color):
    # Remove transparency (https://stackoverflow.com/a/35859141/10712525)
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        alpha = image.convert("RGBA").getchannel("A")
        color = PIL.ImageColor.getrgb(background_color) + (255,)
        new_image = PIL.Image.new("RGBA", image.size, color)
        new_image.paste(image, mask=alpha)
        return new_image

    return image


class ImageData(NamedTuple):
    path: str
    width: int
    height: int


def generate_images(*, config: dict):
    images = []

    if 'favicon_ico' in config:
        # favicon ico version
        images.append(
            File2(
                path=config['output_folder_path'] / 'favicon.ico',
                data=config["favicon_ico"],
            )
        )

    if 'favicon_png' in config:
        images_data = (
            # favicon png version
            ImageData(path=config['static_folder_path'] / 'favicon_16x16.png', width=16, height=16),
            ImageData(path=config['static_folder_path'] / 'favicon_32x32.png', width=32, height=32),
            ImageData(path=config['static_folder_path'] / 'favicon_96x96.png', width=96, height=96),
            ImageData(path=config['static_folder_path'] / 'favicon_192x192.png', width=192, height=192),
            ImageData(path=config['static_folder_path'] / 'favicon_194x194.png', width=194, height=194),

            # ms icon
            ImageData(path=config['static_folder_path'] / 'ms-icon_144x144.png', width=144, height=144),

            # apple icon
            ImageData(path=config['static_folder_path'] / 'apple-touch-icon_57x57.png', width=57, height=57),
            ImageData(path=config['static_folder_path'] / 'apple-touch-icon_60x60.png', width=60, height=60),
            ImageData(path=config['static_folder_path'] / 'apple-touch-icon_72x72.png', width=72, height=72),
            ImageData(path=config['static_folder_path'] / 'apple-touch-icon_76x76.png', width=76, height=76),
            ImageData(path=config['static_folder_path'] / 'apple-touch-icon_114x114.png', width=114, height=114),
            ImageData(path=config['static_folder_path'] / 'apple-touch-icon_120x120.png', width=120, height=120),
            ImageData(path=config['static_folder_path'] / 'apple-touch-icon_128x128.png', width=128, height=128),
            ImageData(path=config['static_folder_path'] / 'apple-touch-icon_144x144.png', width=144, height=144),
            ImageData(path=config['static_folder_path'] / 'apple-touch-icon_152x152.png', width=152, height=152),
            ImageData(path=config['static_folder_path'] / 'apple-touch-icon_167x167.png', width=167, height=167),
            ImageData(path=config['static_folder_path'] / 'apple-touch-icon_180x180.png', width=180, height=180),
            ImageData(path=config['static_folder_path'] / 'apple-touch-icon_195x195.png', width=195, height=195),
            ImageData(path=config['static_folder_path'] / 'apple-touch-icon_196x196.png', width=196, height=196),
            ImageData(path=config['static_folder_path'] / 'apple-touch-icon_228x228.png', width=228, height=228),
            ImageData(path=config['static_folder_path'] / 'apple-touch-icon_512x512.png', width=512, height=512),
            ImageData(path=config['static_folder_path'] / 'apple-touch-icon_1024x1024.png', width=1024, height=1024),

            # browserconfig
            ImageData(path=config['static_folder_path'] / 'browserconfig_30x30.png', width=30, height=30),
            ImageData(path=config['static_folder_path'] / 'browserconfig_44x44.png', width=44, height=44),
            ImageData(path=config['static_folder_path'] / 'browserconfig_70x70.png', width=70, height=70),
            ImageData(path=config['static_folder_path'] / 'browserconfig_150x150.png', width=150, height=150),
            ImageData(path=config['static_folder_path'] / 'browserconfig_310x150.png', width=310, height=150),
            ImageData(path=config['static_folder_path'] / 'browserconfig_310x310.png', width=310, height=310),

            # manifest
            ImageData(path=config['static_folder_path'] / 'manifest_192x192.png', width=192, height=192),
            ImageData(path=config['static_folder_path'] / 'manifest_512x512.png', width=512, height=512),

            # opensearch
            ImageData(path=config['static_folder_path'] / 'opensearch_16x16.png', width=16, height=16),
        )
        images.extend(
            File2(
                path=image.path,
                data=resize_image(image=config["favicon_png"], width=image.width, height=image.height),
            ) for image in images_data
        )

        images_data = (
            # yandex
            ImageData(path=config['static_folder_path'] / 'yandex.png', width=120, height=120),

            # apple startup image
            # Source: https://github.com/onderceylan/pwa-asset-generator
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_1024x1024.png', width=1024, height=1024),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_2048x2732.png', width=2048, height=2732),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_2732x2048.png', width=2732, height=2048),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_1668x2388.png', width=1668, height=2388),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_2388x1668.png', width=2388, height=1668),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_1668x2224.png', width=1668, height=2224),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_2224x1668.png', width=2224, height=1668),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_1536x2048.png', width=1536, height=2048),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_2048x1536.png', width=2048, height=1536),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_1242x2688.png', width=1242, height=2688),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_2688x1242.png', width=2688, height=1242),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_1125x2436.png', width=1125, height=2436),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_2436x1125.png', width=2436, height=1125),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_828x1792.png', width=828, height=1792),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_1792x828.png', width=1792, height=828),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_1242x2208.png', width=1242, height=2208),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_2208x1242.png', width=2208, height=1242),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_750x1334.png', width=750, height=1334),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_1334x750.png', width=1334, height=750),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_640x1136.png', width=640, height=1136),
            ImageData(path=config['static_folder_path'] / 'apple-touch-startup-image_1136x640.png', width=1136, height=640),
        )
        if 'background_color' in config:
            images.extend(
                File2(
                    data=remove_transparency(
                        image=resize_image(image=config["favicon_png"], width=image.width, height=image.height),
                        background_color=config['background_color']
                    ),
                    path=image.path
                )
                for image in images_data
            )
        else:
            images.extend(
            File2(
                path=image.path,
                data=resize_image(image=config["favicon_png"], width=image.width, height=image.height),
            ) for image in images_data
        )

    if 'favicon_svg' in config:
        images.append(
            File2(
                path=config['static_folder_path'] / 'mask-icon.svg',
                data=config["favicon_svg"],
            )
        )

    if 'preview_png' in config:
        images_data = (
            # og
            ImageData(path=config['static_folder_path'] / 'og.png', width=600, height=600),
            ImageData(path=config['static_folder_path'] / 'og.png', width=1080, height=1080),

            # twitter
            ImageData(path=config['static_folder_path'] / 'twitter.png', width=600, height=600),
        )
        images.extend(
            File2(
                path=image.path,
                data=resize_image(image=config["favicon_png"], width=image.width, height=image.height),
            ) for image in images_data
        )

    return images


def generate_templates(*, config: dict):
    generate_index()

def generate_files(*, config: dict):
    """
    verificar las imágenes

    generar_html
    -> Retorna:
        txt files to generate
        image files to generate
    """
    return (
        *generate_images(config=config)
        *generate_templates(config=config)
    )




class Dir:
    """
    doc
    """

    def __init__(
        self,
        *,
        name: str,
    ) -> NoReturn:
        self.name = name
        self.elements = {}

    def add_element(
        self,
        *,
        element: Union[Dir, File],
    ) -> Dir:
        """
        doc
        """
        if isinstance(element, File) or element.name not in self.elements:
            self.elements[element.name] = element
        else:
            self.elements[element.name].elements.update(element.elements)
        return self


class File:
    """
    doc
    """

    def __init__(
        self,
        *,
        name: str,
        data: bytes,
    ) -> NoReturn:
        self.name = name
        self.data = data


def get_tree_part(
    *,
    parts: List[str],
    data: bytes,
) -> Union[Dir, File]:
    """doc"""
    if parts[1:]:
        return Dir(name=parts[0]).add_element(element=get_tree_part(parts=parts[1:], data=data))
    else:
        return File(name=parts[0], data=data)


def get_files_tree(
    *,
    files_to_create: Dir,
) -> Dir:
    base_path = Dir(name='')
    for file in files_to_create:
        base_path.add_element(element=get_tree_part(parts=pathlib.Path(file.path).parts, data=file.data))
    return base_path


def parse_files_tree(
    *,
    files_tree: Dir,
    base_path: pathlib.Path,
) -> NoReturn:
    """
    doc
    """
    for name, element in sorted(files_tree.elements.items()):
        destination_path = base_path / name
        if isinstance(element, File):
            print(destination_path)
            destination_path.write_bytes(element.data)
        else:
            if not destination_path.exists():
                destination_path.mkdir()
            parse_files_tree(files_tree=element, base_path=destination_path)


def create_files(
    *,
    files_to_create,
) -> NoReturn:
    """
    doc
    """
    parse_files_tree(
        files_tree=get_files_tree(files_to_create=files_to_create),
        base_path=pathlib.Path(''),
    )
