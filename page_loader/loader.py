import logging
import logging.config
import os
from typing import List

from page_loader import http, localizer, name

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'standart': {
            'format': '%(asctime)s - %(levelname)s: %(message)s'
        },
        'error': {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'filename': 'page_loader.log',
            'mode': 'a',
            'maxBytes': 10240,
            'backupCount': 0,
            'formatter': 'standart',
        },
        'error_handler': {
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
            'stream': 'ext://sys.stderr',
            'formatter': 'error',
        },
    },
    'loggers': {
        __name__: {
            'handlers': ['file_handler', 'error_handler'],
            'level': 'DEBUG',
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
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
    response = http.get(url)

    logger.info('Get resources from page.')
    local_page, resources = localizer.get_page_and_resources(response)

    logger.info('Write html page file.')
    output_page_file_path = _save_page(local_page, response.url, output_path)

    logger.info('Start download resources.')
    _download_resources(resources, response.url, output_path)

    return output_page_file_path


def _download_resources(
    resource_urls: List[str],
    page_url: str,
    output_path: str
):
    local_res_dir = name.get_local_res_dir(page_url)
    full_path_res_dir = os.path.join(output_path, local_res_dir)

    try:
        os.mkdir(full_path_res_dir)
    except OSError:
        err_msg = 'OSError: directory {dir} is not maked'.format(
            dir=full_path_res_dir
        )
        logger.error(err_msg)
        raise OSError(err_msg)

    for res_url in resource_urls:
        data = http.get(res_url, is_html=False)
        file_name = name.get_for_res_file(page_url, res_url)
        res_file_path = os.path.join(full_path_res_dir, file_name)
        _save_bytes(data.content, res_file_path)


def _save_page(page_data: str, page_url: str, output_path: str) -> str:
    output_page_file_path = os.path.join(
        output_path,
        name.get_for_page_file(page_url)
    )
    _save_bytes(page_data.encode('UTF-8'), output_page_file_path)

    return output_page_file_path


def _save_bytes(
    data: bytes,
    output_path: str
) -> str:
    """Save the html page to disk."""
    try:
        with open(output_path, 'wb') as output_file:
            output_file.write(data)
    except Exception as e:
        logger.error('{ex}: {path}'.format(
            ex=type(e).__name__,
            path=output_path
        ))
        raise e
    return output_path


def _add_scheme(url: str) -> str:
    if '://' not in url:
        return 'http://' + url
    return url
