#!/usr/bin/env python3
"""Page-loader script."""

import argparse
from typing import Tuple
from page_loader import download
import os
import sys
import logging
import logging.config

DESCRIPTION = 'Dowload page'
HELP_STRING = 'Path to download'


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
        'std_handler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout',
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
        'script': {
            'handlers': ['std_handler', 'error_handler'],
            'level': 'DEBUG',
        }
    },
}


def main():
    """Page-loader script."""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger('script')
    url, output_path = get_arguments()
    try:
        print(download(url, output_path))
    except Exception as e:
        logger.debug(e)
        sys.exit(1)
    sys.exit(0)


def get_arguments() -> Tuple[str, str]:
    """Take the command-line arguments.
    url, output

    Returns:
        (url, output_path)
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('url', type=str)
    parser.add_argument(
        '-o', '--output',
        help=HELP_STRING,
        type=str,
        default=os.getcwd()
    )
    args = parser.parse_args()
    return (str(args.url), str(args.output))


if __name__ == "__main__":
    main()
