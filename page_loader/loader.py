import os

from page_loader.localizer import download_resources
from page_loader.parser import get_url_data
from page_loader.net import get_response_content


def download(url: str, output_path: str = os.getcwd()) -> str:
    """Download the page from the url and save it to the output address.
    Return:
        Full path to file.
    """
    url_data = get_url_data(url)

    response = get_response_content(url_data['full_url'])

    page = download_resources(
        response.decode(),
        url_data,
        output_path
    )

    output_file_path = save_page(url_data['file_name'], page, output_path)

    return output_file_path


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
