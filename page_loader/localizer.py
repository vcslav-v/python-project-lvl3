import os
from requests import Response
from typing import List, Tuple
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup
from progress.bar import Bar

from page_loader import name

RESOURCES_TAGS = {'img', 'link', 'script'}
RES_ATTR = {'src', 'href'}


def get_page_and_resources(response: Response) -> Tuple[str, List[str]]:
    """Localize the resources page."""
    soup = BeautifulSoup(response.content.decode(), 'html.parser')
    tags = soup.find_all(RESOURCES_TAGS)
    local_res_dir = name.get_local_res_dir(response.url)
    resources = []
    bar = Bar('Parsing resources', max=len(tags))
    for tag in tags:
        bar.next()
        local_attr, resource = _localize_tag(
            tag.attrs,
            response.url,
            local_res_dir
        )
        if resource:
            tag.attrs.update(local_attr)
            resources.append(resource)
    bar.finish()
    return soup.prettify(formatter='html5'), resources


def _localize_tag(
    attrs: dict,
    page_url: str,
    local_res_dir: str,
) -> Tuple[dict, str]:
    """Localize tag attrs."""
    src_key_set = attrs.keys() & RES_ATTR
    if not src_key_set:
        return {}, ''

    src_key: str = src_key_set.pop()
    if not _is_local_resource(attrs[src_key], page_url):
        return {}, ''

    resource_url = urljoin(page_url, attrs[src_key])
    file_name = name.get_for_res_file(page_url, resource_url)
    return {src_key: os.path.join(local_res_dir, file_name)}, resource_url


def _is_local_resource(value: str, page_url: str) -> bool:
    if not isinstance(value, str):
        return False

    value_netloc = urlparse(value).netloc
    page_netloc = urlparse(page_url).netloc
    return not value_netloc or value_netloc == page_netloc
