"""
Handle templates generation.
"""
from __future__ import annotations

import hashlib
import pathlib
import re
from typing import Any
from typing import List
from typing import Union

import jinja2

from cushead.generator import config as generator_config
from cushead.generator import files
from cushead.generator.templates.jinja import filters


class TemplateLoader:
    """
    Handle jinja templates.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize a jinja template loader.
        """
        template_loader = jinja2.FileSystemLoader(searchpath=str(pathlib.Path(__file__).parent / "jinja/templates"))
        self.template_parser = jinja2.Environment(
            loader=template_loader,
            lstrip_blocks=True,
            autoescape=True,
            **kwargs,
        )

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
    template_loader = TemplateLoader(extensions=["cushead.generator.templates.jinja.extensions.OneLineExtension"])
    template_loader.template_parser.globals["config"] = config
    template_loader.template_parser.filters["generate_sri"] = filters.generate_sri
    index_template = template_loader.render_template(path="index.jinja2")
    index_hash = get_template_hash(template=index_template)
    template_loader.template_parser.globals["index_hash"] = index_hash

    templates = [
        files.File(
            path=config["output_folder_path"] / "index.html",
            data=index_template,
        ),
        files.File(
            path=config["output_folder_path"] / "manifest.json",
            data=template_loader.render_template(path="manifest.jinja2"),
        ),
        files.File(
            path=config["output_folder_path"] / "robots.txt",
            data=template_loader.render_template(path="robots.jinja2"),
        ),
        files.File(
            path=config["output_folder_path"] / "sw.js",
            data=template_loader.render_template(path="sw.jinja2"),
        ),
        files.File(
            path=config["output_folder_path"] / "static" / "early_script.js",
            data=template_loader.render_template(path="early_script.jinja2"),
        ),
        files.File(
            path=config["output_folder_path"] / "static" / "late_script.js",
            data=template_loader.render_template(path="late_script.jinja2"),
        ),
        files.File(
            path=config["output_folder_path"] / "static" / "styles.css",
            data=template_loader.render_template(path="styles.jinja2"),
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
