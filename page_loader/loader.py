import os
import re
from urllib.parse import urlparse

import requests

from page_loader.localizer import download_resources, normalize_name

TYPE_TO_EXTENSIONS = {
    'text/html': 'html'
}

RE_URL = (
    r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]+)([\/\w \.-]*)*\/?(\??(.?)*)$'
)

ERROR_RESPONSE_STATUS = 'response status {status}'
ERROR_CONTENT_TYPE = 'It is not possible to process this type of content'
ERROR_NOT_URL = '{url} is not a url'


def download(url: str, output_path: str = os.getcwd()) -> str:
    """Download the page from the url and save it to the output address.
    Return:
        Full path to file.
    """
    url_data = get_url_data(url)

    response = get_page(url_data)

    url_name = get_url_name(url_data)

    page = download_resources(
        response.content.decode(),
        url_data,
        output_path,
        url_name
    )

    output_file_path = save_page(url_name, page, output_path)

    return output_file_path


def get_page(url: dict) -> requests.models.Response:
    """Load the page."""
    try:
        with requests.Session() as session:
            response = session.get(url['full_url'])
    except Exception as e:
        raise e

    if response.status_code != 200:
        raise ConnectionError(
            ERROR_RESPONSE_STATUS.format(status=response.status_code)
        )

    content_type = response.headers['Content-Type'].split(';')[0].strip()

    if content_type != 'text/html':
        raise ValueError(ERROR_CONTENT_TYPE)

    return response


def save_page(
    url_name: str,
    page: str,
    output_path: str
) -> str:
    """Save the html page to disk."""
    file_name = '{url_name}.html'.format(
        url_name=url_name
    )

    output_file_path = os.path.join(
        output_path,
        file_name
    )

    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write(page)
    except Exception as e:
        raise e

    return output_file_path


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

    return url_data


def get_url_name(url: dict) -> str:
    """Generate the page name by url."""
    parsed_path, _ = os.path.splitext(url['path'])
    without_scheme_url = url['netloc'] + parsed_path
    return normalize_name(without_scheme_url)
