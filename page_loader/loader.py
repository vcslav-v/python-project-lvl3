import os

import requests

from page_loader.localizer import download_resources
from page_loader.parser import get_url_data

TYPE_TO_EXTENSIONS = {
    'text/html': 'html'
}


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

    page = download_resources(
        response.content.decode(),
        url_data,
        output_path
    )

    output_file_path = save_page(url_data['file_name'], page, output_path)

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
