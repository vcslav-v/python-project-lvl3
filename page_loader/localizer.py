import os
from typing import Tuple
from urllib.parse import urlparse
from page_loader.parser import normalize_name

import requests
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
    for child in tags:
        child.attrs = localize_src(
            child.attrs,
            url,
            output_path
        )
    return soup.prettify(formatter='html5')


def localize_src(
    attrs: dict,
    url: dict,
    output_path: str
) -> dict:
    """Localize imgs page."""
    for attr, value in attrs.items():
        if is_local_resource(attr, value, url['netloc']):
            resource_url, resource_name = get_resource_url_name(
                value,
                url
            )
            attrs[attr] = download_resource(
                resource_url,
                resource_name,
                url['file_name'],
                output_path
            )
    return attrs


def is_local_resource(attr: str, value: str, netloc: str) -> bool:
    if not isinstance(value, str) or attr not in RES_ATTR:
        return False

    parsed_value_url = urlparse(value)
    if parsed_value_url.netloc and netloc != parsed_value_url.netloc:
        return False

    _, extention = os.path.splitext(parsed_value_url.path.strip('/'))

    return extention != ''


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


def download_resource(
    url: str,
    file_name: str,
    url_name: str,
    output_path: str
) -> str:
    """Save the resource to disk and return the new path."""
    output_dir_name = '{url_name}_files'.format(
        url_name=url_name
    )
    full_resources_output_path = os.path.join(output_path, output_dir_name)

    img = requests.get(url)

    if not os.path.exists(full_resources_output_path) or (
        not os.path.isdir(full_resources_output_path)
    ):
        os.mkdir(full_resources_output_path)

    file_path = os.path.join(full_resources_output_path, file_name)
    local_file_path = os.path.join(output_dir_name, file_name)

    with open(file_path, 'wb') as img_file:
        img_file.write(img.content)

    return local_file_path
