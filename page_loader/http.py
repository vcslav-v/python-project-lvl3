import requests
from page_loader.logger import logger

ERROR_RESPONSE_STATUS = 'Response code is {status}. URL is {url}'
ERROR_CONTENT_TYPE = 'In response is not html document. URL is {url}'


def get(url: str, is_html=True) -> bytes:
    """Load the content."""
    try:
        with requests.Session() as session:
            response = session.get(url)
    except Exception as e:
        logger.error('{ex}: URL is {url}'.format(
            ex=type(e).__name__, url=url)
        )
        raise e
    response.raise_for_status()

    if is_html:
        content_type = response.headers.get('Content-Type')

        if 'text/html' not in str(content_type):
            logger.warning(ERROR_CONTENT_TYPE.format(url=url))

    return response.content
