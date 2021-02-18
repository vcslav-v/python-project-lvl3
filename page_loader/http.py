import logging
from typing import Generator
import requests

from page_loader import errors

logger = logging.getLogger(__name__)

CHUNK_SIZE = 256


def get_page(url: str) -> bytes:
    """Load the content."""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.error('{e}: URL is {url}'.format(url=url, e=type(exc).__name__))
        raise errors.NetError('cant connect to {url}'.format(url=url)) from exc

    content_type = response.headers.get('Content-Type')
    if 'text/html' not in str(content_type):
        logger.warning(
            'In response is not html text. URL is {url}'.format(url=url)
        )

    return response.content


def get_resource_chunks(url: str) -> Generator:
    """Download a resource via an iterator with chunk."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.error('{e}: URL is {url}'.format(url=url, e=type(exc).__name__))
        raise errors.NetError('cant connect to {url}'.format(url=url)) from exc

    def chunks() -> Generator:
        try:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                yield chunk
        except requests.RequestException as exc:
            logger.error(
                '{e}: URL is {url}'.format(url=url, e=type(exc).__name__)
            )
            raise errors.NetError(
                'cant connect to {url}'.format(url=url)
            ) from exc

    return chunks()
