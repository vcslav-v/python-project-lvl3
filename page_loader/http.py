import requests
from logging import Logger

ERROR_RESPONSE_STATUS = 'Response code is {status}. URL is {url}'
ERROR_CONTENT_TYPE = 'In response is not html document. URL is {url}'


def get(url: str, logger: Logger, is_html=True) -> bytes:
    """Load the content."""
    try:
        with requests.Session() as session:
            response = session.get(url)
    except ConnectionError:
        logger.error('ConnectionError: URL is {url}'.format(url=url))
        raise ConnectionError('URL is {url}'.format(url=url))
    response.raise_for_status()

    if is_html:
        content_type = response.headers.get('Content-Type')

        if 'text/html' not in str(content_type):
            logger.warning(ERROR_CONTENT_TYPE.format(url=url))

    return response.content
