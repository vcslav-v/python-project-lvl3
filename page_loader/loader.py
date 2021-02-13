import logging
import logging.config
import os
from typing import List

from progress.bar import Bar

from page_loader import http, localizer, names, parsed_url

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
        'root': {
            'handlers': ['file_handler', 'error_handler'],
            'level': 'DEBUG',
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('root')


def download(url: str, output_path: str = os.getcwd()) -> str:
    """Download the page from the url and save it to the output address.
    Return:
        Full path to file.
    """
    logger.info('Program started. URL is {url}. {out_path}'.format(
        url=url,
        out_path=output_path
    ))

    url_info = parsed_url.get(url)

    logger.info('Request to {url}'.format(url=url_info['full_url']))
    page_data = http.get(url_info['full_url'], logger).decode()

    logger.info('Get resources from page.')
    local_res_dir = '{url_name}_files'.format(
        url_name=names.get_for_url(url_info['netloc'], url_info['path'])
    )
    page_data, resources = localizer.get_page_and_resources(
        url_info,
        page_data,
        local_res_dir,
        output_path
    )

    logger.info('Write html page file.')
    output_page_file_path = _save_page(page_data, output_path, url_info)

    logger.info('Start download resources.')
    for resource in resources:
        resource['data'] = http.get(
            resource['full_url'], logger, is_html=False
        )

    logger.info('Write resource files.')
    _save_resources(resources, output_path, local_res_dir)

    return output_page_file_path


def _save_resources(
    resources: List[dict], output_path: str, local_res_dir: str
):
    full_path_res_dir = os.path.join(output_path, local_res_dir)
    if not os.path.exists(full_path_res_dir) or (
        not os.path.isdir(full_path_res_dir)
    ):
        try:
            os.mkdir(full_path_res_dir)
        except Exception as e:
            logger.error('{ex}: directory {dir} is not maked'.format(
                ex=type(e).__name__,
                dir=full_path_res_dir
            ))
            raise e
    bar = Bar('Save resources', max=len(resources))
    for resource in resources:
        bar.next()
        _save_bytes(resource['data'], os.path.join(
            full_path_res_dir, resource['file_name'])
        )
    bar.finish()


def _save_page(page_data: str, output_path: str, url_info: dict) -> str:
    output_page_file_path = os.path.join(
        output_path,
        '{url_name}.html'.format(
            url_name=names.get_for_url(url_info['netloc'], url_info['path'])
        ),
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
