import logging
import os
from typing import List
from urllib.parse import urlparse

from progress.bar import Bar

from page_loader import errors, http, localizer, name

logger = logging.getLogger(__name__)


def download(url: str, output_path: str = os.getcwd()) -> str:
    """Download the page from the url and save it to the output address.
    Return:
        Full path to file.
    """
    logger.info('Program started. URL is {url}. {out_path}'.format(
        url=url,
        out_path=output_path
    ))
    url = _add_scheme(url)

    logger.info('Request to {url}'.format(url=url))
    response = http.get_page(url)

    logger.info('Get resources from page.')
    local_page, resources = localizer.get_page_and_resources(response, url)

    logger.info('Write html page file.')
    output_page_file_path = _save_page(local_page, url, output_path)

    logger.info('Start download resources.')
    _download_and_save_resources(resources, url, output_path)

    return output_page_file_path


def _download_and_save_resources(
    resource_urls: List[str],
    page_url: str,
    output_path: str
):
    """Download and save resources."""
    local_res_dir = name.get_local_res_dir(page_url)
    full_path_res_dir = os.path.join(output_path, local_res_dir)

    try:
        os.mkdir(full_path_res_dir)
    except OSError as exc:
        logger.error('{exc}: directory {dir} is not maked'.format(
            exc=type(exc).__name__,
            dir=full_path_res_dir
        ))
        raise errors.SaveError('Directory {dir} cant be maked'.format(
            dir=full_path_res_dir
        )) from exc

    bar = Bar('Download resources', max=len(resource_urls))
    for res_url in resource_urls:
        data_chunks = http.get_resource_chunks(res_url)
        file_name = name.get_for_res_file(page_url, res_url)
        res_file_path = os.path.join(full_path_res_dir, file_name)
        try:
            with open(res_file_path, 'wb') as output_file:
                for data_chunk in data_chunks:
                    output_file.write(data_chunk)
        except OSError as exc:
            logger.error('{exc}: {path}'.format(
                exc=type(exc).__name__,
                path=output_path
            ))
            raise errors.SaveError(
                'File {path} cant be save.'.format(path=output_path)
            ) from exc
        bar.next()
    bar.finish()


def _save_page(page_data: str, page_url: str, output_path: str) -> str:
    """Save the html page."""
    output_page_file_path = os.path.join(
        output_path,
        name.get_for_page_file(page_url)
    )
    try:
        with open(output_page_file_path, 'wb') as output_file:
            output_file.write(page_data.encode('UTF-8'))
    except OSError as exc:
        logger.error('{exc}: {path}'.format(
            exc=type(exc).__name__,
            path=output_path
        ))
        raise errors.SaveError(
            'File {path} cant be save.'.format(path=output_path)
        ) from exc

    return output_page_file_path


def _add_scheme(url: str) -> str:
    """Add a schema if it doesn't exist."""
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return 'http://' + url
    return url
