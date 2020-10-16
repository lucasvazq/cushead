#!/usr/bin/env python3
"""
Test CLI interactions
"""
import pathlib
import unittest

from src.console import console


OUTPUT_FILE = str(pathlib.Path(__file__).parent / "output/settings.json")


class TestConsole(unittest.TestCase):
    """
    Main console interactions.
    """


    def test_valid_args(self):
        """
        Test valid input args.
        """
        console.parse_args(args=["-d", "-i", OUTPUT_FILE])
        console.parse_args(args=["-c", OUTPUT_FILE])


if __name__ == "__main__":
    unittest.main()
