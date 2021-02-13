import re
from urllib.parse import urlparse
import os
from page_loader.logger import logger

RE_URL = (
    r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]+)([\/\w \.-]*)*\/?(\??(.?)*)$'
)


def get(url: str) -> dict:
    """Check the validity of the url, make data dict.
    Returns:
    {scheme, netloc, path, query, full_url, file_name, res_dir_name}
    """
    re_checked_url = re.search(RE_URL, url, flags=re.I)

    if not re_checked_url:
        logger.warning('{url} is not a url'.format(url=url))

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

    return url_data


def get_for_res(
    value: str,
    url: dict
) -> dict:
    """Generate the resource info.
    {'url', 'file_name', 'local_path'}
    """
    parsed_value_url = urlparse(value)

    parsed_path, extention = os.path.splitext(parsed_value_url.path)

    if not extention:
        extention = '.html'

    if not parsed_value_url.scheme and parsed_value_url.path[0] == '/':
        res_url = '{scheme}{netloc}{path}{query}'.format(
            scheme=url['scheme'],
            netloc=url['netloc'],
            path=parsed_value_url.path,
            query=(
                '?' + parsed_value_url.query if parsed_value_url.query else ''
            ),
        )
    elif not parsed_value_url.scheme:
        res_url = '{scheme}{netloc}{path}{local_path}{query}'.format(
            scheme=url['scheme'],
            netloc=url['netloc'],
            path=url['path'],
            local_path=parsed_value_url.path,
            query=(
                '?' + parsed_value_url.query if parsed_value_url.query else ''
            ),
        )
    else:
        res_url = value

    return {
        'full_url': res_url,
        'path': parsed_path,
        'extention': extention
    }
