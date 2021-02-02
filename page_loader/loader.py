import os
import re
from urllib.parse import urlparse

import requests

TYPE_TO_EXTENSIONS = {
    'text/html': 'html'
}

RE_URL = r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]+)([\/\w \.-]*)*\/?$'
RE_NOT_NUMS_OR_LETTERS = r'[^a-z0-9]+'

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

    output_file_path = save_page(prepared_url, response, output_path)

    return output_file_path


def get_page(url: str) -> requests.models.Response:
    try:
        with requests.Session() as session:
            response = session.get(url)
    except Exception as e:
        raise e

    if response.status_code != 200:
        raise ConnectionError(
            ERROR_RESPONSE_STATUS.format(status=response.status_code)
        )

    return response


def save_page(
    url: str,
    response: requests.models.Response,
    output_path: str
) -> str:
    output_file_path = os.path.join(
        output_path,
        make_file_name(url, response.headers['Content-Type'])
    )

    with open(output_file_path, 'w') as output_file:
        output_file.write(response.text)

    return output_file_path


def make_file_name(url: str, raw_content_type: str) -> str:
    """Make a file name from the url.
    Example:
    https://google.com -> google-com.html
    """
    content_type = raw_content_type.split(';')[0]
    if content_type in TYPE_TO_EXTENSIONS:
        extension = TYPE_TO_EXTENSIONS[content_type]
    else:
        raise ValueError(ERROR_CONTENT_TYPE)

    parsed_url = urlparse(url)
    parsed_path, _ = os.path.splitext(parsed_url.path)
    without_scheme_url = parsed_url.netloc + parsed_path

    file_name = '{name}.{extension}'.format(
        name=re.sub(
            RE_NOT_NUMS_OR_LETTERS,
            "-",
            without_scheme_url,
            flags=re.I
        ),
        extension=extension
    )
    return file_name


def prepare_url(url: str) -> str:
    re_checked_url = re.search(RE_URL, url, flags=re.I)

    if not re_checked_url:
        raise ValueError('{url} is not a url'.format(url=url))

    parsed_url = urlparse(url)

    if not parsed_url.scheme:
        return 'http://' + url
    return url
