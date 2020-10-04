#!/usr/bin/env python3
"""
Main script thats run the CLI feature.
"""
import sys
from typing import NoReturn

from src.console import console


def main() -> NoReturn:
    """
    Handle the CLI feature.
    """
    console.show_presentation()
    console.parse_args(args=sys.argv[1:])


if __name__ == "__main__":
    main()
