import os
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from progress.bar import Bar

from page_loader.logger import logger
from page_loader.net import get_response_content
from page_loader import parser

RESOURCES_TAGS = {'img', 'link', 'script'}
RES_ATTR = {'src', 'href'}


def localize_resources(
    url: dict,
    output_path: str,
) -> str:
    """Localize the resources page."""
    soup = BeautifulSoup(url['data'], 'html.parser')
    tags = soup.find_all(RESOURCES_TAGS)
    logger.debug(tags)
    bar = Bar('Load resources', max=len(tags))
    local_res_dir = '{url_name}_files'.format(
        url_name=parser.get_file_name(url)
    )
    full_path_res_dir = os.path.join(output_path, local_res_dir)
    for tag in tags:
        bar.next()
        tag.attrs = _localize_tag(
            tag.attrs,
            url,
            local_res_dir,
            full_path_res_dir
        )
    bar.finish()
    return soup.prettify(formatter='html5')


def _localize_tag(
    attrs: dict,
    url: dict,
    local_res_dir,
    full_path_res_dir: str
) -> dict:
    """Localize tag attrs."""
    for attr, value in attrs.items():
        if _is_local_resource(attr, value, url['netloc']):
            res_info = parser.get_resource_info(
                value,
                url
            )

            res_info['file_name'] = parser.get_resource_file_name(
                url, res_info
            )

            logger.info(
                'Request resource - {url}'.format(url=res_info['full_url'])
            )
            res_info['data'] = get_response_content(
                res_info['full_url'],
                is_html=False,
            )

            logger.info(
                'Save resource - {file_name}'.format(
                    file_name=res_info['file_name']
                )
            )
            _save_resource(
                res_info,
                full_path_res_dir,
            )
            attrs[attr] = os.path.join(local_res_dir, res_info['file_name'])
    return attrs


def _save_resource(
    res: dict,
    output_res_dir: str
):
    """Save the resource to disk."""

    if not os.path.exists(output_res_dir) or (
        not os.path.isdir(output_res_dir)
    ):
        try:
            os.mkdir(output_res_dir)
        except Exception as e:
            logger.error('{ex}: directory {dir} is not maked'.format(
                ex=type(e).__name__,
                dir=output_res_dir
            ))
            raise e

    file_path = os.path.join(output_res_dir, res['file_name'])

    try:
        with open(file_path, 'wb') as res_file:
            res_file.write(res['data'])
    except Exception as e:
        logger.error('{ex}: file {path} is not saved'.format(
            ex=type(e).__name__,
            path=file_path
        ))
        raise e


def _is_local_resource(attr: str, value: str, netloc: str) -> bool:
    if not isinstance(value, str) or attr not in RES_ATTR:
        return False

    parsed_value_url = urlparse(value)
    if parsed_value_url.netloc and netloc != parsed_value_url.netloc:
        return False
    return True
