"""
Handle jinja filters.
"""
import base64
import hashlib

from cushead.generator.templates import templates


def generate_sri(path: str) -> str:
    """
    Generate the SHA-512 Subresource Integrity of a file.

    Args:
        path: the template path, relative to the templates_folder instance attribute.

    Returns:
        The Subresource Integrity.
    """
    template_loader = templates.TemplateLoader()
    data = template_loader.render_template(path=path)
    digest = hashlib.new("sha512", data).digest()
    base64_digest = base64.standard_b64encode(digest).decode("ascii")
    return f"sha512-{base64_digest}"
