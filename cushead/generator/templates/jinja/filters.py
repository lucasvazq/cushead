"""
Handle jinja functions.
"""
import base64
import hashlib


def generate_sri(path: str) -> str:
    """
    Generate the Subresource Integrity of a file.

    Args:
        path: the file.

    Returns:
        The Subresource Integrity.
    """
    with open(path) as file:
        digest = hashlib.new("sha512", file.read().encode()).digest()
        base64_digest = base64.standard_b64encode(digest).decode("ascii")
        return f"sha512-{base64_digest}"
