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
    prepared_url = prepare_url(url)

    response = get_page(prepared_url)

    url_name = get_url_name(prepared_url)

    page = download_resources(
        response.content.decode(),
        prepared_url,
        output_path,
        url_name
    )

    output_file_path = save_page(url_name, page, output_path)

    return output_file_path


def get_page(url: str) -> requests.models.Response:
    """Load the page."""
    try:
        with requests.Session() as session:
            response = session.get(url)
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


def prepare_url(url: str) -> str:
    """Check the validity of the url, and add a schema if not."""
    re_checked_url = re.search(RE_URL, url, flags=re.I)

    if not re_checked_url:
        raise ValueError('{url} is not a url'.format(url=url))

    parsed_url = urlparse(url)

    if not parsed_url.scheme:
        return 'http://' + url
    return url


def get_url_name(url: str) -> str:
    """Generate the page name by url."""
    parsed_url = urlparse(url)
    parsed_path, _ = os.path.splitext(parsed_url.path)
    without_scheme_url = parsed_url.netloc + parsed_path
    without_scheme_url = without_scheme_url.rstrip('/')
    return normalize_name(without_scheme_url)
