import os
from typing import List, Tuple
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup
from progress.bar import Bar

from page_loader import url

RESOURCES_TAGS = {'img', 'link', 'script'}
RES_ATTR = {'src', 'href'}


def make_local_html(
    response: bytes, page_url: str, local_res_dir: str
) -> Tuple[str, List[str]]:
    """Localize the resources page."""
    soup = BeautifulSoup(response.decode(), 'html.parser')
    tags = soup.find_all(RESOURCES_TAGS)
    resources = []
    bar = Bar('Parsing resources', max=len(tags))
    for tag in tags:
        bar.next()
        tag.attrs, resource = _localize_tag(
            tag.attrs,
            page_url,
            local_res_dir
        )
        if resource:
            resources.append(resource)
    bar.finish()
    return soup.prettify(formatter='html5'), resources


def _localize_tag(
    attrs: dict,
    page_url: str,
    local_res_dir: str,
) -> Tuple[dict, str]:
    """Find and make a local tag with a resource."""
    local_attrs = attrs.copy()
    src_key_set = local_attrs.keys() & RES_ATTR
    if not src_key_set:
        return attrs, ''

    src_key: str = src_key_set.pop()
    if not _is_local_resource(local_attrs[src_key], page_url):
        return attrs, ''

    resource_url = urljoin(page_url, attrs[src_key])
    file_name = url.to_res_filename(page_url, resource_url)
    local_attrs[src_key] = os.path.join(local_res_dir, file_name)
    return local_attrs, resource_url


def _is_local_resource(value: str, page_url: str) -> bool:
    if not isinstance(value, str):
        return False

    value_netloc = urlparse(value).netloc
    page_netloc = urlparse(page_url).netloc
    return not value_netloc or value_netloc == page_netloc
