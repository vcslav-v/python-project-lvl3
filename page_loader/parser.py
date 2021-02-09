import re
from urllib.parse import urlparse
import os
from page_loader.logger import logger

RE_URL = (
    r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]+)([\/\w \.-]*)*\/?(\??(.?)*)$'
)
RE_NOT_NUMS_OR_LETTERS = r'[^a-z0-9]+'


def get_url_info(url: str) -> dict:
    """Check the validity of the url, make data dict.
    Returns:
    {scheme, netloc, path, query, full_url, file_name, res_dir_name}
    """
    re_checked_url = re.search(RE_URL, url, flags=re.I)

    if not re_checked_url:
        logger.error('{url} is not a url'.format(url=url))
        raise ValueError('{url} is not an url'.format(url=url))

    if '://' not in url:
        url = 'http://' + url

    parsed_url = urlparse(url)

    url_data = {
        'netloc': parsed_url.netloc,
        'path': parsed_url.path.rstrip('/'),
        'query': parsed_url.query
    }

    url_data['scheme'] = parsed_url.scheme + '://'
    url_data['full_url'] = parsed_url.geturl()

    url_data['file_name'] = get_url_name(url_data)
    url_data['assets_prefix'] = normalize_name(url_data['netloc'])
    url_data['res_dir_name'] = url_data['file_name'] + '_files'

    return url_data


def get_url_name(url: dict) -> str:
    """Generate the page name by url."""
    parsed_path, _ = os.path.splitext(url['path'])
    without_scheme_url = url['netloc'] + parsed_path
    return normalize_name(without_scheme_url)


def get_resource_info(
    value: str,
    url: dict
) -> dict:
    """Generate the resource info.
    {'url', 'file_name', 'local_path'}
    """
    parsed_value_url = urlparse(value)

    parsed_path, extention = os.path.splitext(parsed_value_url.path.strip('/'))

    if not extention:
        extention = '.html'

    file_name = '{prefix}-{name}{extention}'.format(
        prefix=url['assets_prefix'],
        name=normalize_name(parsed_path),
        extention=extention
    )

    if not parsed_value_url.scheme:
        res_url = '{scheme}{netloc}{path}{query}'.format(
            scheme=url['scheme'],
            netloc=url['netloc'],
            path=parsed_value_url.path,
            query=(
                '?' + parsed_value_url.query if parsed_value_url.query else ''
            ),
        )
    else:
        res_url = value

    local_path = os.path.join(
        '{url_name}_files'.format(url_name=url['file_name']),
        file_name
    )

    return {
        'url': res_url,
        'file_name': file_name,
        'local_path': local_path
    }


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
