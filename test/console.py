#!/usr/bin/env python3
"""
Test CLI interactions.
"""
import io
import pathlib
import unittest
from contextlib import redirect_stderr
from typing import List
from typing import Tuple

import colorama

from src import info
from src.console import arguments
from src.console import console


class TestConsole(unittest.TestCase):
    """
    Main console interactions.
    """

    def setUp(self) -> None:
        """
        Setup common variables.
        """
        self.output_file = pathlib.Path(__file__).parent / "output/settings.json"

    def execute_args(self, *, args: List[str], output: str, exception_expected: bool = False) -> None:
        """
        Run the console with the given arguments.

        Args:
            args: the arguments.
            output: expected output.
            exception_expected: if an exception is expected.
        """
        with io.StringIO() as buf, redirect_stderr(buf):
            if exception_expected:
                with self.assertRaises(SystemExit) as exception:
                    console.parse_args(args=args)
                self.assertIsInstance(exception.exception, SystemExit)
            else:
                console.parse_args(args=args)

            if output:
                self.assertEqual(buf.getvalue(), (
                    f"usage: {arguments.USAGE}\n"
                    f"{info.PACKAGE_NAME}: error: {output}\n"
                ))

    def test_valid_args(self) -> None:
        """
        Test valid input args.
        """
        self.execute_args(args=["-d", "-i", str(self.output_file)], output="")
        self.execute_args(args=["-c", str(self.output_file)], output="")

    def test_invalid_args(self) -> None:
        """
        Test invalid args setup.
        """

        # Missing arguments.
        self.execute_args(args=[""], output="Miss Required arguments. Use -c or -d. Use -h for help.", exception_expected=True)

        # Invalid combination.
        self.execute_args(args=["-c", "-d"], output="Can't use -c and -d arguments together.", exception_expected=True)

        # Execute optional command without a required arg.
        self.execute_args(args=["-c", "-i"], output="Can't use -i without -d.", exception_expected=True)

        # Missing FILE.
        self.execute_args(args=["-c"], output="Miss FILE", exception_expected=True)

        # Inexistent file.
        reference = pathlib.Path(__file__).parent / "inexistent_file.json"
        output = (
            f"The file ({reference}) must be referred to a path that exists.\n"
            f"ABSOLUTE PATH: {reference.absolute()}"
        )
        self.execute_args(args=["-c", str(reference)], output=output, exception_expected=True)

        # Reference must be a file, not a directory.
        reference = pathlib.Path(__file__).parent
        output = (
            f"The file ({reference}) must be referred to a file path.\n"
            f"ABSOLUTE PATH: {reference.absolute()}"
        )
        self.execute_args(args=["-c", str(reference)], output=output, exception_expected=True)


if __name__ == "__main__":
    unittest.main()
