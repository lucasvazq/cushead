#!/usr/bin/env python3
"""
Test CLI interactions.
"""
import contextlib
import io
import json
import os
import pathlib
import shutil
import unittest
from typing import List

from src import info
from src.console import arguments
from src.console import console


class ExecuteArgs(unittest.TestCase):
    """
    doc
    """

    def __init__(self, *args, **kwargs):
        """
        doc
        """
        super().__init__(*args, **kwargs)
        self.maxDiff = None
        self.output_folder = pathlib.Path(__file__).parent / "output"
        self.output_file = self.output_folder / "settings.json"

    def setUp(self) -> None:
        """
        doc
        """
        os.makedirs(self.output_folder)
        self.execute_args(args=["-d", "-i", str(self.output_file)])
        self.config = console.get_default_config()

    def tearDown(self) -> None:
        """
        doc
        """
        if self.output_folder.exists():
            shutil.rmtree(self.output_folder.absolute())

    def write_config_file(self) -> None:
        self.output_file.write_text(json.dumps(self.config))

    def execute_args(self, *, args: List[str], output: str = "", exception_expected: bool = False) -> None:
        """
        Run the console with the given arguments.

        Args:
            args: the arguments.
            output: expected output.
            exception_expected: if an exception is expected.
        """
        with io.StringIO() as stderr, contextlib.redirect_stderr(stderr):
            if exception_expected:
                with self.assertRaises(SystemExit) as exception:
                    console.parse_args(args=args)
                self.assertIsInstance(exception.exception, SystemExit)
            else:
                console.parse_args(args=args)

            if output:
                self.assertEqual(stderr.getvalue(), (
                    f"usage: {arguments.USAGE}\n"
                    f"{info.PACKAGE_NAME}: error: {output}\n"
                ))
            else:
                self.assertEqual(stderr.getvalue(), "")


class TestArgs(ExecuteArgs):
    """
    doc
    """

    def test_valid_args(self) -> None:
        """
        doc
        remove this
        """
        self.execute_args(args=["-d", "-i", str(self.output_file)])
        self.execute_args(args=["-c", str(self.output_file)])

    def test_invalid_args(self) -> None:
        """
        doc
        """
        # Missing arguments.
        self.execute_args(args=[""], output="Miss Required arguments. Use -c or -d. Use -h for help.", exception_expected=True)

        # Invalid combination.
        self.execute_args(args=["-c", "-d"], output="Can't use -c and -d arguments together.", exception_expected=True)

        # Execute optional command without a required arg.
        self.execute_args(args=["-c", "-i"], output="Can't use -i without -d.", exception_expected=True)

        # Missing FILE.
        self.execute_args(args=["-c"], output="Miss FILE", exception_expected=True)


class ZZZZTestConfig(ExecuteArgs):
    """
    doc
    """

    def test_missing_key(self) -> None:
        """
        doc
        """
        return

    def atest_invalid_data_type(self) -> None:
        """
        doc
        """
        self.config["favicon_ico"] = 1
        output= (
            "Key 'favicon_ico' error:\n"
            "Or(None, <class 'str'>) did not validate 1\n"
            "1 should be instance of 'str'"
        )
        self.write_config_file()
        self.execute_args(args=["-c", str(self.output_file)], output=output, exception_expected=True)

    def atest_invalid_key(self) -> None:
        """
        doc
        """
        self.config["invalid_key"] = ""
        self.write_config_file()
        self.execute_args(args=["-c", str(self.output_file)], output=f"Wrong key 'invalid_key' in {self.config}", exception_expected=True)

    def atest_color_related_keys(self) -> None:
        """
        doc
        """
        # Test valid values
        self.assertEqual(self.config["main_color"], "#ff0000")
        self.assertEqual(self.config["background_color"], "#ffffff")
        self.write_config_file()
        self.execute_args(args=["-c", str(self.output_file)], output=f"Wrong key 'invalid_key' in {self.config}", exception_expected=True)

        self.config = console.get_default_config()
        self.config["main_color"] = "#ffff"
        self.write_config_file()
        self.execute_args(args=["-c", str(self.output_file)], output="The key main_color must be a hex color code. If you don't want any value on this key, set the value to null.", exception_expected=True)

        self.config = console.get_default_config()
        self.config["background_color"] = "#ffff"
        self.write_config_file()
        self.execute_args(args=["-c", str(self.output_file)], output="The key background_color must be a hex color code. If you don't want any value on this key, set the value to null.", exception_expected=True)

    def atest_image_reference_is_not_a_image_file(self) -> None:
        """
        doc
        """
        reference = self.output_folder / "favicon_ico_16px.ico"
        self.assertTrue(reference.exists())
        reference.write_bytes(b"")
        output = (
            f"Can't identify as image the favicon_ico reference ({reference})\n"
            f"Exception: cannot identify image file '{reference.absolute()}'"
        )
        self.execute_args(args=["-c", str(self.output_file)], output=output, exception_expected=True)


class TestReferences(ExecuteArgs):
    """
    doc
    """

    def test_inexistent_file(self) -> None:
        """
        doc
        """
        reference = pathlib.Path(__file__).parent / "inexistent_file.json"
        output = (
            f"The file ({reference}) must be referred to a path that exists.\n"
            f"ABSOLUTE PATH: {reference.absolute()}"
        )
        self.execute_args(args=["-c", str(reference)], output=output, exception_expected=True)

    def test_config_reference_is_directory(self) -> None:
        """
        doc
        """
        output = (
            f"The file ({self.output_folder}) must be referred to a file path.\n"
            f"ABSOLUTE PATH: {self.output_folder.absolute()}"
        )
        self.execute_args(args=["-c", str(self.output_folder)], output=output, exception_expected=True)

    def test_invalid_format(self) -> None:
        """
        doc
        """
        self.output_file.write_text("invalid file format")
        output = (
            f"Invalid json file format in ({self.output_file})\n"
            f"ABSOLUTE PATH: {self.output_file.absolute()}\n"
            "Exception: Expecting value: line 1 column 1 (char 0)"
        )
        self.execute_args(args=["-c", str(self.output_file)], output=output, exception_expected=True)

    def test_image_does_not_exists(self) -> None:
        """
        doc
        """
        reference = self.output_folder / "favicon_ico_16px.ico"
        os.remove(reference)
        output = (
            f"favicon_ico reference ({reference}) doesn't exists\n"
            f"ABSOLUTE PATH: {reference.absolute()}"
        )
        self.execute_args(args=["-c", str(self.output_file)], output=output, exception_expected=True)

    def test_image_reference_is_directory(self) -> None:
        """
        doc
        """
        reference = self.output_folder / "favicon_ico_16px.ico"
        os.remove(reference)
        os.makedirs(reference)
        output = (
            f"favicon_ico reference ({reference}) must be a file, not a directory\n"
            f"Exception: [Errno 21] Is a directory: '{reference.absolute()}'"
        )
        self.execute_args(args=["-c", str(self.output_file)], output=output, exception_expected=True)

    def test_image_reference_is_not_a_image_file(self) -> None:
        """
        doc
        """
        reference = self.output_folder / "favicon_ico_16px.ico"
        reference.write_bytes(b"")
        output = (
            f"Can't identify as image the favicon_ico reference ({reference})\n"
            f"Exception: cannot identify image file '{reference.absolute()}'"
        )
        self.execute_args(args=["-c", str(self.output_file)], output=output, exception_expected=True)

    def test_invalid_image_format(self) -> None:
        """
        doc
        """
        return


class TestFileCreation(ExecuteArgs):
    """
    doc
    """

    def test_file_creation(self) -> None:
        """
        doc
        """
        reference = self.output_folder / "directory"
        os.mkdir(reference)
        self.execute_args(args=["-d", str(reference)])


if __name__ == "__main__":
    unittest.main()
