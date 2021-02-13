import os
import re

RE_NOT_NUMS_OR_LETTERS = r'[^a-z0-9]+'


def get_for_url(url: dict) -> str:
    """Generate the page name by url."""
    parsed_path, _ = os.path.splitext(url['path'])
    without_scheme_url = url['netloc'] + parsed_path
    return _normalize_name(without_scheme_url)


def get_for_res(netloc: str, path: str, extention: str):
    return '{name}{extention}'.format(
        name=_normalize_name(netloc + path),
        extention=extention
    )


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
