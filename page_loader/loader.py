import os

from page_loader.localizer import localize_resources
from page_loader.parser import get_url_info
from page_loader.net import get_response_content
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

    url_info = get_url_info(url)

    logger.info('Request to {url}'.format(url=url_info['full_url']))
    response = get_response_content(url_info['full_url'])

    logger.info('Start download resources.')
    page = localize_resources(
        response.decode(),
        url_info,
        output_path
    )

    logger.info('Write html page file.')
    output_file_path = save_page(url_info['file_name'], page, output_path)
    return output_file_path


def save_page(
    url_file_name: str,
    page: str,
    output_path: str
) -> str:
    """Save the html page to disk."""
    file_name = '{url_name}.html'.format(
        url_name=url_file_name
    )

    output_file_path = os.path.join(
        output_path,
        file_name
    )

    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write(page)
    except Exception as e:
        logger.error('{ex}: {path}'.format(
            ex=type(e).__name__,
            path=output_file_path
        ))
        raise e
    return output_file_path
