import os

from page_loader import http, localizer, names, parsed_url
from page_loader.logger import logger


def download(url: str, output_path: str = os.getcwd()) -> str:
    """Download the page from the url and save it to the output address.
    Return:
        Full path to file.
    """
    logger.info('Program started. URL is {url}. {out_path}'.format(
        url=url,
        out_path=output_path
    ))

    page_info = parsed_url.get(url)

    logger.info('Request to {url}'.format(url=page_info['full_url']))
    page_info['data'] = http.get(page_info['full_url']).decode()
    page_info['file_name'] = '{url_name}.html'.format(
        url_name=names.get_for_url(page_info)
    )

    logger.info('Start download resources.')
    page_info['data'] = localizer.get_page(
        page_info,
        output_path
    )

    logger.info('Write html page file.')
    output_file_path = _save_page(page_info, output_path)
    return output_file_path


def _save_page(
    page_info: dict,
    output_path: str
) -> str:
    """Save the html page to disk."""
    output_file_path = os.path.join(
        output_path,
        page_info['file_name']
    )

    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write(page_info['data'])
    except Exception as e:
        logger.error('{ex}: {path}'.format(
            ex=type(e).__name__,
            path=output_file_path
        ))
        raise e
    return output_file_path
