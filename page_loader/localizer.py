import os
from requests import Response
from typing import List, Tuple
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup
from progress.bar import Bar

from page_loader import names

RESOURCES_TAGS = {'img', 'link', 'script'}
RES_ATTR = {'src', 'href'}


def get_page_and_resources(response: Response) -> Tuple[str, List[str]]:
    """Localize the resources page."""
    soup = BeautifulSoup(response.content.decode(), 'html.parser')
    tags = soup.find_all(RESOURCES_TAGS)
    local_res_dir = names.get_local_res_dir(response.url)
    resources = []
    bar = Bar('Parsing resources', max=len(tags))
    for tag in tags:
        bar.next()
        tag.attrs, resource = _localize_tag(
            tag.attrs,
            response.url,
            local_res_dir
        )
        if resource:
            resources.append(resource)
    bar.finish()
    return soup.prettify(formatter='html5'), resources


def _localize_tag(
    attrs: dict,
    url: str,
    local_res_dir: str,
) -> Tuple[dict, str]:
    """Localize tag attrs."""
    resource = ''
    for attr, value in attrs.items():
        if _is_local_resource(attr, value, url):
            resource = urljoin(url, value)
            file_name = names.get_for_res(url, resource)
            attrs[attr] = os.path.join(local_res_dir, file_name)
    return attrs, resource


def _is_local_resource(attr: str, value: str, page_url: str) -> bool:
    if not isinstance(value, str) or attr not in RES_ATTR:
        return False

    value_netloc = urlparse(value).netloc
    page_netloc = urlparse(page_url).netloc
    if value_netloc and value_netloc != page_netloc:
        return False
    return True
