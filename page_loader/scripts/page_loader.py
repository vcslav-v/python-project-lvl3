#!/usr/bin/env python3
"""Page-loader script."""

import argparse
import logging.config
import os
import sys
from typing import Tuple

from page_loader import download, errors

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
        __name__: {
            'handlers': ['file_handler', 'error_handler'],
            'level': 'DEBUG',
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)


def main():
    """Page-loader script."""
    url, output_path = get_arguments()
    exit_status = 0
    try:
        print(download(url, output_path))
    except errors.AppInternalError:
        exit_status = 1
    sys.exit(exit_status)


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
    return (args.url, args.output)


if __name__ == "__main__":
    main()
