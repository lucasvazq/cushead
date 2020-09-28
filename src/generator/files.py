#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc
"""
import hashlib
import io
import pathlib
from typing import NamedTuple

import jinja2
import PIL
from resizeimage import resizeimage


class Image(NamedTuple):
    """
    doc
    """
    reference: str
    name: str
    data: bytes


class File(NamedTuple):
    """
    doc
    """
    path: str
    data: bytes


def resize_image(*, image: str, width: int, height: int):
    """
    doc
    """
    resized_image = resizeimage.resize_contain(image, (width, height))
    resized_image.format = image.format
    return resized_image


def remove_transparency(*, image, background_color):
    """
    doc
    """
    # Remove transparency (https://stackoverflow.com/a/35859141/10712525)
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        alpha = image.convert("RGBA").getchannel("A")
        color = PIL.ImageColor.getrgb(background_color) + (255,)
        new_image = PIL.Image.new("RGBA", image.size, color)
        new_image.paste(image, mask=alpha)
        new_image.format = image.format
        return new_image
    return image


class ImageData(NamedTuple):
    """
    doc
    """
    path: str
    width: int
    height: int


def convert_image_to_bytes(image):
    io_file = io.BytesIO()
    image.save(io_file, format=image.format)
    return io_file.read()


def generate_images(*, config: dict):
    """
    doc
    """
    images = []

    if 'favicon_ico' in config:
        images.append(
            # favicon ico version, used for opensearch too
            File(
                path=config['output_folder_path'] / 'favicon.ico',
                data=convert_image_to_bytes(config["favicon_ico"]),
            )
        )

    if 'favicon_png' in config:
        images_data = (
            # favicon png version
            ImageData(path=config['output_folder_path'] / 'static' / 'favicon-16x16.png', width=16, height=16),
            ImageData(path=config['output_folder_path'] / 'static' / 'favicon-32x32.png', width=32, height=32),
            ImageData(path=config['output_folder_path'] / 'static' / 'favicon-96x96.png', width=96, height=96),
            ImageData(path=config['output_folder_path'] / 'static' / 'favicon-192x192.png', width=192, height=192),
            ImageData(path=config['output_folder_path'] / 'static' / 'favicon-194x194.png', width=194, height=194),

            # apple icon
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-icon-57x57.png', width=57, height=57),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-icon-60x60.png', width=60, height=60),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-icon-72x72.png', width=72, height=72),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-icon-76x76.png', width=76, height=76),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-icon-114x114.png', width=114, height=114),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-icon-120x120.png', width=120, height=120),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-icon-128x128.png', width=128, height=128),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-icon-144x144.png', width=144, height=144),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-icon-152x152.png', width=152, height=152),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-icon-167x167.png', width=167, height=167),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-icon-180x180.png', width=180, height=180),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-icon-195x195.png', width=195, height=195),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-icon-196x196.png', width=196, height=196),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-icon-228x228.png', width=228, height=228),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-icon-512x512.png', width=512, height=512),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-icon-1024x1024.png', width=1024, height=1024),

            # browserconfig
            ImageData(path=config['output_folder_path'] / 'static' / 'browserconfig-30x30.png', width=30, height=30),
            ImageData(path=config['output_folder_path'] / 'static' / 'browserconfig-44x44.png', width=44, height=44),
            ImageData(path=config['output_folder_path'] / 'static' / 'browserconfig-70x70.png', width=70, height=70),
            ImageData(path=config['output_folder_path'] / 'static' / 'browserconfig-150x150.png', width=150, height=150),
            ImageData(path=config['output_folder_path'] / 'static' / 'browserconfig-310x150.png', width=310, height=150),
            ImageData(path=config['output_folder_path'] / 'static' / 'browserconfig-310x310.png', width=310, height=310),
            ImageData(path=config['output_folder_path'] / 'static' / 'browserconfig-144x144.png', width=144, height=144),

            # manifest
            ImageData(path=config['output_folder_path'] / 'static' / 'manifest-192x192.png', width=192, height=192),
            ImageData(path=config['output_folder_path'] / 'static' / 'manifest-512x512.png', width=512, height=512),

            # opensearch
            ImageData(path=config['output_folder_path'] / 'static' / 'opensearch-16x16.png', width=16, height=16),
        )
        images.extend(
            File(
                path=image.path,
                data=convert_image_to_bytes(resize_image(image=config["favicon_png"], width=image.width, height=image.height)),
            ) for image in images_data
        )

        images_data = (
            # yandex
            ImageData(path=config['output_folder_path'] / 'static' / 'yandex.png', width=120, height=120),

            # apple startup image
            # Source: https://github.com/onderceylan/pwa-asset-generator
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-1024x1024.png', width=1024, height=1024),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-2048x2732.png', width=2048, height=2732),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-2732x2048.png', width=2732, height=2048),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-1668x2388.png', width=1668, height=2388),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-2388x1668.png', width=2388, height=1668),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-1668x2224.png', width=1668, height=2224),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-2224x1668.png', width=2224, height=1668),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-1536x2048.png', width=1536, height=2048),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-2048x1536.png', width=2048, height=1536),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-1242x2688.png', width=1242, height=2688),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-2688x1242.png', width=2688, height=1242),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-1125x2436.png', width=1125, height=2436),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-2436x1125.png', width=2436, height=1125),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-828x1792.png', width=828, height=1792),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-1792x828.png', width=1792, height=828),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-1242x2208.png', width=1242, height=2208),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-2208x1242.png', width=2208, height=1242),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-750x1334.png', width=750, height=1334),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-1334x750.png', width=1334, height=750),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-640x1136.png', width=640, height=1136),
            ImageData(path=config['output_folder_path'] / 'static' / 'apple-touch-startup-image-1136x640.png', width=1136, height=640),
        )
        if 'background_color' in config:
            images.extend(
                File(
                    data=convert_image_to_bytes(remove_transparency(
                        image=resize_image(image=config["favicon_png"], width=image.width, height=image.height),
                        background_color=config['background_color']
                    )),
                    path=image.path
                ) for image in images_data
            )
        else:
            images.extend(
            File(
                path=image.path,
                data=convert_image_to_bytes(resize_image(image=config["favicon_png"], width=image.width, height=image.height)),
            ) for image in images_data
        )

    if 'favicon_svg' in config:
        images.append(
            File(
                path=config['output_folder_path'] / 'static' / 'mask-icon.svg',
                data=config["favicon_svg"].read_bytes(),
            )
        )

    if 'preview_png' in config:
        images_data = (
            # Estas imagenes se sobreescriben, evitar que ocurra eso
            # og
            ImageData(path=config['output_folder_path'] / 'static' / 'preview-600x600.png', width=600, height=600),
            ImageData(path=config['output_folder_path'] / 'static' / 'preview-1080x1080.png', width=1080, height=1080),

            # twitter
            ImageData(path=config['output_folder_path'] / 'static' / 'preview-600x600.png', width=600, height=600),

            # microdata
            ImageData(path=config['output_folder_path'] / 'static' / 'preview-600x600.png', width=600, height=600),
        )
        images.extend(
            File(
                path=image.path,
                data=convert_image_to_bytes(resize_image(image=config["favicon_png"], width=image.width, height=image.height)),
            ) for image in images_data
        )

    return images


class TemplateLoader:
    """
    doc
    """

    def __init__(self, *, templates_path):
        template_loader = jinja2.FileSystemLoader(searchpath=templates_path)
        self.template_parser = jinja2.Environment(loader=template_loader, extensions=['src.generator.jinja_extension.OneLineExtension'])
        self.template_parser.lstrip_blocks = True

    def add_template_variable(self, **variables: dict):
        """
        doc
        """
        self.template_parser.globals.update(**variables)

    def load_template(self, *, path):
        """
        doc
        """
        return self.template_parser.get_template(path).render().encode('utf-8')


def generate_template_hash(*, template) -> str:
    """
    doc
    """
    return hashlib.sha1(template).hexdigest()[0:6]


def generate_templates(*, config: dict):
    templates_path = pathlib.Path(pathlib.Path(__file__).parent, 'templates')
    template_loader = TemplateLoader(templates_path=templates_path)
    template_loader.add_template_variable(**{'config': config})
    index_template = template_loader.load_template(path='index.html')
    index_hash = generate_template_hash(template=index_template)
    template_loader.add_template_variable(**{'index_hash': index_hash})

    templates = [
        File(
            path=config['output_folder_path'] / 'index.html',
            data=index_template
        ),
        File(
            path=config['output_folder_path'] / 'robots.txt',
            data=template_loader.load_template(path='robots.html')
        ),
        File(
            path=config['output_folder_path'] / 'static' / 'manifest.json',
            data=template_loader.load_template(path='manifest.html')
        ),
        File(
            path=config['output_folder_path'] / 'static' / 'sw.js',
            data=template_loader.load_template(path='service_worker.html')
        ),
    ]

    if "domain" in config:
        templates.extend((
            File(
                path=config['output_folder_path'] / 'sitemap.xml',
                data=template_loader.load_template(path='sitemap.html')
            ),
            File(
                path=config['output_folder_path'] / 'static' / 'opensearch.xml',
                data=template_loader.load_template(path='opensearch.html')
            ),
        ))

    if "favicon_png" in config or "main_color" in config:
        templates.append(
            File(
                path=config['output_folder_path'] / 'static' / 'browserconfig.xml',
                data=template_loader.load_template(path='browserconfig.html')
            )
        )

    if "author_email" in config:
        templates.append(
            File(
                path=config['output_folder_path'] / '.well-known' /'security',
                data=template_loader.load_template(path='security.html')
            )
        )

    if "author_name" in config or "author_email" in config:
        templates.append(
            File(
                path=config['output_folder_path'] / 'humans.txt',
                data=template_loader.load_template(path='humans.html')
            )
        )

    return templates

def generate_files(*, config: dict):
    """
    doc
    """
    files = (
        *generate_images(config=config),
        *generate_templates(config=config),
    )
    return files
