#!/usr/bin/env python3
"""
Main script thats run the CLI feature.
"""
import sys
from typing import List

from src.console import console
from src.console import logs


def main(*, args: List[str]) -> None:
    """
    Handle the CLI feature.
    """
    logs.show_presentation()
    console.parse_args(args=args)


if __name__ == "__main__":
    main(args=sys.argv[1:])
