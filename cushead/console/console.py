#!/usr/bin/env python3
"""
Run the CLI functionality.
"""
import sys
from typing import List

from cushead.console import logs
from cushead.console.arguments import execute


def init(*, args: List[str]) -> None:
    """
    Execute the CLI functionality.

    Args:
        args: list of arguments.
    """
    logs.show_presentation()
    execute.parse_args(args=args)


def main() -> None:
    """
    Handle the CLI feature.
    """
    init(args=sys.argv[1:])


if __name__ == "__main__":
    main()
