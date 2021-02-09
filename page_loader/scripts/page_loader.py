#!/usr/bin/env python3
"""Page-loader script."""

import argparse
from typing import Tuple
from page_loader import download
import os
import sys

DESCRIPTION = 'Dowload page'
HELP_STRING = 'Path to download'
EXC = {
    'KeyError': 1,
    'TabError': 2,
    'NameError': 3,
    'TypeError': 4,
    'IndexError': 5,
    'ValueError': 6,
    'BufferError': 7,
    'ImportError': 8,
    'LookupError': 9,
    'MemoryError': 10,
    'SyntaxError': 11,
    'SystemError': 12,
    'RuntimeError': 13,
    'TimeoutError': 14,
    'UnicodeError': 15,
    'OverflowError': 16,
    'AssertionError': 17,
    'AttributeError': 18,
    'RecursionError': 19,
    'ReferenceError': 20,
    'FileExistsError': 21,
    'ArithmeticError': 22,
    'BrokenPipeError': 23,
    'ConnectionError': 24,
    'PermissionError': 25,
    'EnvironmentError': 26,
    'IndentationError': 27,
    'InterruptedError': 28,
    'ChildProcessError': 29,
    'FileNotFoundError': 30,
    'IsADirectoryError': 31,
    'UnboundLocalError': 32,
    'FloatingPointError': 33,
    'NotADirectoryError': 34,
    'ProcessLookupError': 35,
    'UnicodeDecodeError': 36,
    'ModuleNotFoundError': 37,
    'NotImplementedError': 38,
    'ConnectionResetError': 39,
    'UnicodeTranslateError': 40,
    'ConnectionAbortedError': 41,
    'ConnectionRefusedError': 42,
    'ZeroDivisionError': 43
}


def main():
    """Page-loader script."""
    url, output_path = get_arguments()
    try:
        download(url, output_path)
    except Exception as e:
        sys.exit(
            EXC[type(e).__name__]
        )
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
