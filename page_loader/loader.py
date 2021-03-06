import logging
import os
from typing import List
from urllib.parse import urlparse
import pathlib

from progress.bar import Bar

from page_loader import errors, http, localizer, url

logger = logging.getLogger(__name__)


def download(page_url: str, output_path: str = os.getcwd()) -> str:
    """Download the page from the url and save it to the output address.
    Return:
        Full path to file.
    """
    logger.info('Program started. URL is {url}. {out_path}'.format(
        url=url,
        out_path=output_path
    ))
    page_url = _add_scheme_if_missing(page_url)

    logger.info('Request to {url}'.format(url=url))
    page_html = http.get_page(page_url)

    local_res_dir = url.to_res_dir_name(page_url)

    logger.info('Get resources from page.')
    local_page_html, resource_urls = localizer.make_local_html(
        page_html, page_url, local_res_dir
    )

    logger.info('Write html page file.')
    output_page_file_path = _save_page(local_page_html, page_url, output_path)

    logger.info('Start download resources.')
    _download_and_save_resources(
        resource_urls, page_url, output_path, local_res_dir
    )

    return output_page_file_path


def _download_and_save_resources(
    resource_urls: List[str],
    page_url: str,
    output_path: str,
    local_res_dir: str,
):
    """Download and save resources."""
    full_path_res_dir = os.path.join(output_path, local_res_dir)

    try:
        pathlib.Path(full_path_res_dir).mkdir(parents=True, exist_ok=True)
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
        file_name = url.to_filename(res_url)
        res_file_path = os.path.join(full_path_res_dir, file_name)
        try:
            data_chunks = http.get_resource_chunks(res_url)
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
        except errors.NetError as exc:
            logger.warning(
                '{e}: cant download resource. URL is {url}'.format(
                    url=url, e=type(exc).__name__
                )
            )
        bar.next()
    bar.finish()


def _save_page(page_html: str, page_url: str, output_path: str) -> str:
    """Save the html page."""
    output_page_file_path = os.path.join(
        output_path,
        url.to_filename(page_url)
    )
    try:
        with open(output_page_file_path, 'w') as output_file:
            output_file.write(page_html)
    except OSError as exc:
        logger.error('{exc}: {path}'.format(
            exc=type(exc).__name__,
            path=output_path
        ))
        raise errors.SaveError(
            'File {path} cant be save.'.format(path=output_path)
        ) from exc

    return output_page_file_path


def _add_scheme_if_missing(url: str) -> str:
    """Add a schema if it doesn't exist."""
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return 'http://' + url
    return url
