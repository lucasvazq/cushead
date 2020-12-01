"""
Handle templates generation.
"""
from __future__ import annotations

import hashlib
import pathlib
import re
from typing import List, Union

import jinja2

from cushead.generator import config as generator_config
from cushead.generator import files


class TemplateLoader:
    """
    Handle jinja2 templates.
    """

    def __init__(self, *, templates_folder: pathlib.Path) -> None:
        """
        Create a template loader of jinja2.

        Args:
            templates_folder: the path where the templates are stored.
        """
        template_loader = jinja2.FileSystemLoader(searchpath=str(templates_folder))
        self.template_parser = jinja2.Environment(
            loader=template_loader,
            lstrip_blocks=True,
            autoescape=True,
            extensions=["cushead.generator.templates.jinja_extension.OneLineExtension"],
        )

    def add_template_variable(
        self, *, name: str, value: Union[generator_config.Config, str]
    ) -> None:
        """
        Add a variable to the template loader context.

        Args:
            name: the variable name.
            value: the variable value.
        """
        self.template_parser.globals.update({name: value})

    def render_template(self, *, path: str) -> bytes:
        """
        Render a template.

        Args:
            path: the template path, relative to the templates_folder instance attribute.

        Returns:
            The template rendered in UTF-8 format.
        """
        rendered_template = self.template_parser.get_template(path).render()
        cleaned_template = re.sub("((\n +)+\n)|(\n\n$)", "\n", rendered_template)
        return cleaned_template.encode()


def get_template_hash(*, template: bytes) -> str:
    """
    Get a hash of a template.

    Args:
        template: the template in UTF-8 format.

    Returns:
        The hash.
    """
    return hashlib.sha256(template).hexdigest()[0:6]


def generate_templates(*, config: generator_config.Config) -> List[files.File]:
    """
    Get templates ready to create.

    Args:
        config: the config used in the templates context.

    Returns:
        The templates.
    """
    templates_folder = pathlib.Path(__file__).parent / "templates"
    template_loader = TemplateLoader(templates_folder=templates_folder)
    template_loader.add_template_variable(name="config", value=config)
    index_template = template_loader.render_template(path="index.jinja2")
    index_hash = get_template_hash(template=index_template)
    template_loader.add_template_variable(name="index_hash", value=index_hash)

    templates = [
        files.File(
            path=config["output_folder_path"] / "index.html",
            data=index_template,
        ),
        files.File(
            path=config["output_folder_path"] / "robots.txt",
            data=template_loader.render_template(path="robots.jinja2"),
        ),
        files.File(
            path=config["output_folder_path"] / "static" / "manifest.json",
            data=template_loader.render_template(path="manifest.jinja2"),
        ),
        files.File(
            path=config["output_folder_path"] / "static" / "sw.js",
            data=template_loader.render_template(path="service_worker.jinja2"),
        ),
    ]

    if config.get("domain"):
        templates.append(
            files.File(
                path=config["output_folder_path"] / "sitemap.xml",
                data=template_loader.render_template(path="sitemap.jinja2"),
            ),
        )
        if config.get("title"):
            templates.append(
                files.File(
                    path=config["output_folder_path"] / "static" / "opensearch.xml",
                    data=template_loader.render_template(path="opensearch.jinja2"),
                ),
            )

    if config.get("favicon_png") or config.get("main_color"):
        templates.append(
            files.File(
                path=config["output_folder_path"] / "static" / "browserconfig.xml",
                data=template_loader.render_template(path="browserconfig.jinja2"),
            )
        )

    if config.get("author_email"):
        templates.append(
            files.File(
                path=config["output_folder_path"] / ".well-known" / "security",
                data=template_loader.render_template(path="security.jinja2"),
            )
        )

    if config.get("author_name") or config.get("author_email"):
        templates.append(
            files.File(
                path=config["output_folder_path"] / "humans.txt",
                data=template_loader.render_template(path="humans.jinja2"),
            )
        )

    return templates
