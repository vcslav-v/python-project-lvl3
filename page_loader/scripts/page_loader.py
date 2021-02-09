#!/usr/bin/env python3
"""Page-loader script."""

import argparse
from typing import Tuple
from page_loader import download
from page_loader.logger import logger
import os
import sys

DESCRIPTION = 'Dowload page'
HELP_STRING = 'Path to download'


def main():
    """Page-loader script."""
    url, output_path = get_arguments()

    try:
        logger.debug('Start')
        print(download(url, output_path))
        logger.debug('End')
    except Exception:
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
