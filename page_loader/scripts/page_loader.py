#!/usr/bin/env python3
"""Page-loader script."""

import argparse
from typing import Tuple
from page_loader import loader
import os
import sys

DESCRIPTION = 'Dowload page'
HELP_STRING = 'Path to download'


def main():
    """Page-loader script."""
    url, output_path = get_arguments()
    try:
        loader.download(url, output_path)
        sys.exit(0)
    except Exception as e:
        loader.logger.debug(type(e).__name__)
        sys.exit(1)


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
