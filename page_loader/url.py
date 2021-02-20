import os
import re
from urllib.parse import urlparse

RE_NOT_NUMS_OR_LETTERS = r'[^a-z0-9]+'


def to_filename(url: str) -> str:
    """Generate the page file name by url."""
    parsed_url = urlparse(url.rstrip('/'))
    without_extention_path, extention = os.path.splitext(parsed_url.path)
    if not extention:
        extention = '.html'
    without_scheme_url = parsed_url.netloc + without_extention_path
    return _normalize_name(without_scheme_url) + extention


def to_res_dir_name(url: str):
    """Generate the resource dir name by url."""
    parsed_url = urlparse(url)
    without_extention_path, _ = os.path.splitext(parsed_url.path)
    without_scheme_url = parsed_url.netloc + without_extention_path
    return _normalize_name(without_scheme_url) + '_files'


def _normalize_name(name: str) -> str:
    """Make a normalize name from the url.
    Example:
    https://google.com -> google-com
    """
    name = re.sub(
        RE_NOT_NUMS_OR_LETTERS,
        "-",
        name,
        flags=re.I
    )
    return name
