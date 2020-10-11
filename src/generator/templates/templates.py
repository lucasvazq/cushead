"""
Handle templates generation.
"""
from __future__ import annotations

import hashlib
import pathlib
from typing import List
from typing import Union

import jinja2

from src.generator import configuration
from src.generator import files


class TemplateLoader:
    """
    Handle the jinja template loader.
    """

    def __init__(self, *, templates_path: pathlib.Path) -> None:
        """
        Create a template loader of jinja2.

        Args:
            templates_path: the path where the templates are stored.
        """
        template_loader = jinja2.FileSystemLoader(searchpath=str(templates_path))
        self.template_parser = jinja2.Environment(
            loader=template_loader,
            lstrip_blocks=True,
            autoescape=True,
            extensions=["src.generator.templates.jinja_extension.OneLineExtension"],
        )

    def add_template_variable(self, name: str, value: Union[configuration.Config, str]) -> None:
        """
        Add variable to the template loader.

        Args:
            name: variable name.
            value: variable value.
        """
        self.template_parser.globals.update({name: value})

    def render_template(self, *, path: str) -> bytes:
        """
        Render a template.

        Args:
            path: template path.

        Returns:
            The template in string format.
        """
        return self.template_parser.get_template(path).render().encode("utf-8")


def generate_template_hash(*, template: bytes) -> str:
    """
    Generate a hash of a template.

    Args:
        template: the template in string format.

    Returns:
        The hash.
    """
    return hashlib.sha256(template).hexdigest()[0:6]


def generate_templates(*, config: configuration.Config) -> List[files.File]:
    """
    Get templates ready to be created.

    Args:
        config: the configuration.

    Returns:
        The templates list.
    """
    templates_path = pathlib.Path(__file__).parent / "templates"
    template_loader = TemplateLoader(templates_path=templates_path)
    template_loader.add_template_variable(name="config", value=config)
    index_template = template_loader.render_template(path="index.jinja2")
    index_hash = generate_template_hash(template=index_template)
    template_loader.add_template_variable(name="index_hash", value=index_hash)

    templates = [
        files.File(
            path=config["output_folder_path"] / "index.jinja2",
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
        templates.extend(
            (
                files.File(
                    path=config["output_folder_path"] / "sitemap.xml",
                    data=template_loader.render_template(path="sitemap.jinja2"),
                ),
                files.File(
                    path=config["output_folder_path"] / "static" / "opensearch.xml",
                    data=template_loader.render_template(path="opensearch.jinja2"),
                ),
            )
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
