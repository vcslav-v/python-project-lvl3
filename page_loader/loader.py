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

    url_info = parsed_url.get(url)

    logger.info('Request to {url}'.format(url=url_info['full_url']))
    page_data = http.get(url_info['full_url']).decode()

    logger.info('Start download resources.')
    page_data = localizer.get_page(
        url_info,
        page_data,
        output_path
    )

    output_page_file_path = os.path.join(
        output_path,
        '{url_name}.html'.format(
            url_name=names.get_for_url(url_info)
        ),
    )
    logger.info('Write html page file.')
    output_file_path = _save(page_data, output_page_file_path)
    return output_file_path


def _save(
    page_data: str,
    output_path: str
) -> str:
    """Save the html page to disk."""
    try:
        with open(output_path, 'w') as output_file:
            output_file.write(page_data)
    except Exception as e:
        logger.error('{ex}: {path}'.format(
            ex=type(e).__name__,
            path=output_path
        ))
        raise e
    return output_path
