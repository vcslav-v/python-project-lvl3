import os
from typing import List, Tuple
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from progress.bar import Bar

from page_loader import names, parsed_url
from page_loader.logger import logger

RESOURCES_TAGS = {'img', 'link', 'script'}
RES_ATTR = {'src', 'href'}


def get_page_and_resources(
    url: dict,
    page_data: str,
    local_res_dir: str,
    output_path: str,
) -> Tuple[str, List[dict]]:
    """Localize the resources page."""
    soup = BeautifulSoup(page_data, 'html.parser')
    tags = soup.find_all(RESOURCES_TAGS)
    logger.debug(tags)
    bar = Bar('Parsing resources', max=len(tags))
    resources = []
    for tag in tags:
        bar.next()
        tag.attrs, resource = _localize_tag(
            tag.attrs,
            url,
            local_res_dir
        )
        if resource:
            resources.append(resource)
    bar.finish()
    return soup.prettify(formatter='html5'), resources


def _localize_tag(
    attrs: dict,
    url: dict,
    local_res_dir: str,
) -> Tuple[dict, dict]:
    """Localize tag attrs."""
    resource = {}
    for attr, value in attrs.items():
        if _is_local_resource(attr, value, url['netloc']):
            resource = parsed_url.get_for_res(
                value,
                url
            )

            resource['file_name'] = names.get_for_res(
                url['netloc'],
                resource['path'],
                resource['extention']
            )
            attrs[attr] = os.path.join(local_res_dir, resource['file_name'])

    return attrs, resource


def _is_local_resource(attr: str, value: str, netloc: str) -> bool:
    if not isinstance(value, str) or attr not in RES_ATTR:
        return False

    parsed_value_url = urlparse(value)
    if parsed_value_url.netloc and netloc != parsed_value_url.netloc:
        return False
    return True
