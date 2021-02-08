import re
from urllib.parse import urlparse
import os
from typing import Tuple

RE_URL = (
    r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]+)([\/\w \.-]*)*\/?(\??(.?)*)$'
)
RE_NOT_NUMS_OR_LETTERS = r'[^a-z0-9]+'


def get_url_data(url: str) -> dict:
    """Check the validity of the url, make data dict.
    Returns:
    {scheme, netloc, path, query, full_url}
    """
    re_checked_url = re.search(RE_URL, url, flags=re.I)

    if not re_checked_url:
        raise ValueError('{url} is not a url'.format(url=url))

    parsed_url = urlparse(url)

    url_data = {
        'netloc': parsed_url.netloc,
        'path': parsed_url.path.rstrip('/'),
        'query': parsed_url.query
    }

    if parsed_url.scheme:
        url_data['scheme'] = parsed_url.scheme + '://'
        url_data['full_url'] = parsed_url.geturl()
    else:
        url_data['scheme'] = 'http://'
        url_data['full_url'] = url_data['scheme'] + parsed_url.geturl()

    url_data['file_name'] = get_url_name(url_data)

    return url_data


def get_url_name(url: dict) -> str:
    """Generate the page name by url."""
    parsed_path, _ = os.path.splitext(url['path'])
    without_scheme_url = url['netloc'] + parsed_path
    return normalize_name(without_scheme_url)


def get_resource_url_name(
    value: str,
    url: dict
) -> Tuple[str, str]:
    """Generate the file name by url."""
    parsed_value_url = urlparse(value)

    parsed_path, extention = os.path.splitext(parsed_value_url.path.strip('/'))
    parsed_value_path = normalize_name(parsed_path) + extention

    if not parsed_value_url.scheme:
        target_address = '{scheme}{netloc}{path}?{query}'.format(
            scheme=url['scheme'],
            netloc=url['netloc'],
            path=parsed_value_url.path,
            query=parsed_value_url.query,
        )
    else:
        target_address = value

    return (target_address, parsed_value_path)


def normalize_name(name: str) -> str:
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