import logging

import requests

from page_loader import errors


def get(url: str, is_html=True) -> requests.Response:
    """Load the content."""
    logger = logging.getLogger(__name__)
    try:
        with requests.Session() as session:
            response = session.get(url)
            response.raise_for_status()
    except requests.RequestException as exc:
        logger.error('{e}: URL is {url}'.format(url=url, e=type(exc).__name__))
        raise errors.NetError('cant connect to {url}'.format(url=url)) from exc

    if is_html:
        content_type = response.headers.get('Content-Type')

        if 'text/html' not in str(content_type):
            logger.warning(
                'In response is not html text. URL is {url}'.format(url=url)
            )

    return response
