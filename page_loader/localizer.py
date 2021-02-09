import os
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from page_loader.net import get_response_content
from page_loader.parser import get_resource_info
from page_loader.logger import logger
from progress.bar import Bar

RESOURCES_TAGS = {'img', 'link', 'script'}
RES_ATTR = {'src', 'href'}


def localize_resources(
    html_text: str,
    url: dict,
    output_path: str,
) -> str:
    """Localize the resources page."""
    soup = BeautifulSoup(html_text, 'lxml')
    logger.debug(html_text)
    tags = soup.find_all(RESOURCES_TAGS)
    logger.debug(tags)
    bar = Bar('Load resources', max=len(tags))
    for tag in tags:
        bar.next()
        tag.attrs = localize_tag(
            tag.attrs,
            url,
            output_path
        )
    bar.finish()
    return soup.prettify(formatter='html5')


def localize_tag(
    attrs: dict,
    url: dict,
    output_path: str
) -> dict:
    """Localize tag attrs."""
    for attr, value in attrs.items():
        if is_local_resource(attr, value, url['netloc']):
            res_info = get_resource_info(
                value,
                url
            )
            logger.info('Request resource - {url}'.format(url=res_info['url']))
            res_info['data'] = get_response_content(
                res_info['url'],
                is_html=False,
            )
            logger.info(
                'Save resource - {file_name}'.format(
                    file_name=res_info['file_name']
                )
            )
            save_resource(
                res_info,
                url,
                output_path,
            )
            attrs[attr] = res_info['local_path']
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
    """Save the resource to disk."""
    full_resources_output_path = os.path.join(
        output_path, url['res_dir_name']
    )

    if not os.path.exists(full_resources_output_path) or (
        not os.path.isdir(full_resources_output_path)
    ):
        try:
            os.mkdir(full_resources_output_path)
        except Exception as e:
            logger.error('{ex}: directory {dir} is not maked'.format(
                ex=type(e).__name__,
                dir=full_resources_output_path
            ))
            raise e

    file_path = os.path.join(full_resources_output_path, res['file_name'])

    try:
        with open(file_path, 'wb') as res_file:
            res_file.write(res['data'])
    except Exception as e:
        logger.error('{ex}: file {path} is not saved'.format(
                ex=type(e).__name__,
                path=file_path
            ))
        raise e
