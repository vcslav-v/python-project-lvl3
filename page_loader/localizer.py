import os
from urllib.parse import urlparse
from page_loader.parser import get_resource_data
from page_loader.net import get_response_content

from bs4 import BeautifulSoup

RESOURCES_TAGS = {'img', 'link', 'script'}
RES_ATTR = {'src', 'href'}


def download_resources(
    html_text: str,
    url: dict,
    output_path: str,
) -> str:
    """Localize the resources page."""
    soup = BeautifulSoup(html_text, 'lxml')
    tags = soup.find_all(RESOURCES_TAGS)
    for tag in tags:
        tag.attrs = localize_src(
            tag.attrs,
            url,
            output_path
        )
    return soup.prettify(formatter='html5')


def localize_src(
    attrs: dict,
    url: dict,
    output_path: str
) -> dict:
    """Localize res page."""
    for attr, value in attrs.items():
        if is_local_resource(attr, value, url['netloc']):
            res_data = get_resource_data(
                value,
                url
            )
            res_data['data'] = get_response_content(
                res_data['url'],
                is_html=False,
            )
            save_resource(
                res_data,
                url,
                output_path,
            )
            attrs[attr] = res_data['local_path']
    return attrs


def is_local_resource(attr: str, value: str, netloc: str) -> bool:
    if not isinstance(value, str) or attr not in RES_ATTR:
        return False

    parsed_value_url = urlparse(value)
    if parsed_value_url.netloc and netloc != parsed_value_url.netloc:
        return False

    _, extention = os.path.splitext(parsed_value_url.path.strip('/'))

    return extention != ''


def save_resource(
    res: dict,
    url: dict,
    output_path: str
):
    """Save the resource to disk and return the new path."""
    full_resources_output_path = os.path.join(
        output_path, url['res_folder_name']
    )

    if not os.path.exists(full_resources_output_path) or (
        not os.path.isdir(full_resources_output_path)
    ):
        os.mkdir(full_resources_output_path)

    file_path = os.path.join(full_resources_output_path, res['file_name'])

    with open(file_path, 'wb') as res_file:
        res_file.write(res['data'])
