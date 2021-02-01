import os
import re
from urllib.parse import urlparse

import requests

TYPE_TO_EXTENSIONS = {
    'text/html': 'html'
}


def download(url: str, output_path: str = os.getcwd()) -> str:
    """Download the page from the url and save it to the output address.
    Return:
        Full path to file.
    """
    checked_url = add_scheme(url)
    with requests.Session() as session:
        response = session.get(checked_url)

    output_file_path = os.path.join(
        output_path,
        make_file_name(checked_url, response.headers['Content-Type'])
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
        raise ValueError('It is not possible to process this type of content')

    parsed_url = urlparse(url)
    parsed_path, _ = os.path.splitext(parsed_url.path)
    without_scheme_url = parsed_url.netloc + parsed_path

    file_name = '{name}.{extension}'.format(
        name=re.sub(
            r'[^a-z0-9]+',
            "-",
            without_scheme_url,
            flags=re.I
        ),
        extension=extension
    )
    return file_name


def add_scheme(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return 'http://' + url
    return url
