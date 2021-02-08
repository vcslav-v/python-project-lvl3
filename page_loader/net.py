import requests
from page_loader.logger import logger

ERROR_RESPONSE_STATUS = 'response status {status}'
ERROR_CONTENT_TYPE = 'It is not possible to process this type of content'


def get_response_content(url: str, is_html=True) -> bytes:
    """Load the content."""
    try:
        with requests.Session() as session:
            response = session.get(url)
    except Exception as e:
        logger.exception('Net error. URL is {url}'.format(url=url))
        raise e

    if response.status_code != 200:
        logger.error('Response code is not 200. URL is {url}'.format(url=url))
        raise ConnectionError(
            ERROR_RESPONSE_STATUS.format(status=response.status_code)
        )

    if is_html:
        content_type = response.headers['Content-Type'].split(';')[0].strip()

        if content_type != 'text/html':
            logger.error(
                'Response is not html document. URL is {url}'.format(url=url)
            )
            raise ValueError(ERROR_CONTENT_TYPE)

    return response.content
