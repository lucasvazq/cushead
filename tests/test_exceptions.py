#!/usr/bin/env python3
"""
Test CLI interactions.
"""
import os
import pathlib
import shutil
import unittest

from cushead.console import console
from tests import base_tests


class BaseExceptionsTests(base_tests.BaseTests):
    """
    doc
    """


class TestArgs(BaseExceptionsTests):
    """
    doc
    """

    def test_valid_args(self) -> None:
        """
        doc
        remove this
        """
        self.execute_args(args=["-d", "-i", str(self.config_file)])
        self.execute_args(args=["-c", str(self.config_file)])

    def test_invalid_args(self) -> None:
        """
        doc
        """
        # Missing arguments.
        self.execute_args(args=[""], expected_exception="Miss Required arguments. Use -c or -d. Use -h for help.")

        # Invalid combination.
        self.execute_args(args=["-c", "-d"], expected_exception="Can't use -c and -d arguments together.")

        # Execute optional command without a required arg.
        self.execute_args(args=["-c", "-i"], expected_exception="Can't use -i without -d.")

        # Missing FILE.
        self.execute_args(args=["-c"], expected_exception="Miss FILE")


class TestConfig(BaseExceptionsTests):
    """
    doc
    """

    def test_missing_key(self) -> None:
        """
        doc
        """
        del self.config["static_url"]
        self.write_config_file()
        self.execute_args(args=["-c", str(self.config_file)], expected_exception="Missing key: 'static_url'")

    def test_invalid_data_type(self) -> None:
        """
        doc
        """
        self.config["favicon_ico"] = 1
        expected_exception = (
            "Key 'favicon_ico' error:\n"
            "Or(None, <class 'str'>) did not validate 1\n"
            "1 should be instance of 'str'"
        )
        self.write_config_file()
        self.execute_args(args=["-c", str(self.config_file)], expected_exception=expected_exception)

    def test_invalid_key(self) -> None:
        """
        doc
        """
        self.config["invalid_key"] = ""
        self.write_config_file()
        self.execute_args(args=["-c", str(self.config_file)], expected_exception=f"Wrong key 'invalid_key' in {self.config}")

    def test_color_related_keys(self) -> None:
        """
        doc
        """
        # Test valid values
        self.assertEqual(self.config["main_color"], "#ff0000")
        self.assertEqual(self.config["background_color"], "#ffffff")
        self.write_config_file()
        self.execute_args(args=["-c", str(self.config_file)])

        self.config = console.get_default_config()
        self.config["main_color"] = "#ffff"
        self.write_config_file()
        self.execute_args(args=["-c", str(self.config_file)], expected_exception="The key main_color must be a hex color code. If you don't want any value on this key, set the value to null.")

        self.config = console.get_default_config()
        self.config["background_color"] = "rgba(255, 255, 255, 0)"
        self.write_config_file()
        self.execute_args(args=["-c", str(self.config_file)], expected_exception="The key background_color must be a hex color code. If you don't want any value on this key, set the value to null.")


class TestReferences(BaseExceptionsTests):
    """
    doc
    """

    def test_inexistent_file(self) -> None:
        """
        doc
        """
        reference = pathlib.Path(__file__).parent / "inexistent_file.json"
        expected_exception = (
            f"The file ({reference}) must be referred to a path that exists.\n"
            f"ABSOLUTE PATH: {reference.absolute()}"
        )
        self.execute_args(args=["-c", str(reference)], expected_exception=expected_exception)

    def test_config_reference_is_directory(self) -> None:
        """
        doc
        """
        expected_exception = (
            f"The file ({self.output_folder}) must be referred to a file path.\n"
            f"ABSOLUTE PATH: {self.output_folder.absolute()}"
        )
        self.execute_args(args=["-c", str(self.output_folder)], expected_exception=expected_exception)

    def test_invalid_format(self) -> None:
        """
        doc
        """
        self.maxDiff = None
        self.config_file.write_text("invalid file format")
        expected_exception = (
            f"Invalid json file format in ({self.config_file})\n"
            f"ABSOLUTE PATH: {self.config_file.absolute()}\n"
            "Exception: Expecting value: line 1 column 1 (char 0)"
        )
        self.execute_args(args=["-c", str(self.config_file)], expected_exception=expected_exception)

    def test_image_does_not_exists(self) -> None:
        """
        doc
        """
        reference = self.output_folder / "favicon_ico_16px.ico"
        os.remove(reference)
        expected_exception = (
            f"favicon_ico reference ({reference}) doesn't exists\n"
            f"ABSOLUTE PATH: {reference.absolute()}"
        )
        self.execute_args(args=["-c", str(self.config_file)], expected_exception=expected_exception)

    def test_image_reference_is_directory(self) -> None:
        """
        doc
        """
        reference = self.output_folder / "favicon_ico_16px.ico"
        os.remove(reference)
        os.makedirs(reference)
        expected_exception = (
            f"favicon_ico reference ({reference}) must be a file, not a directory\n"
            f"Exception: [Errno 21] Is a directory: '{reference.absolute()}'"
        )
        self.execute_args(args=["-c", str(self.config_file)], expected_exception=expected_exception)

    def test_image_reference_is_not_a_image_file(self) -> None:
        """
        doc
        """
        reference = self.output_folder / "favicon_ico_16px.ico"
        reference.write_bytes(b"")
        expected_exception = (
            f"Can't identify as image the favicon_ico reference ({reference})\n"
            f"Exception: cannot identify image file '{reference.absolute()}'"
        )
        self.execute_args(args=["-c", str(self.config_file)], expected_exception=expected_exception)

    def test_invalid_image_format(self) -> None:
        """
        doc
        """
        reference = self.output_folder / "favicon_ico_16px.ico"
        shutil.copy(self.output_folder / "favicon_png_2688px.png", reference)
        expected_exception = (
            f"The favicon_ico reference ({reference}) has a wrong image format.\n"
            f"Expected ICO, but received PNG\n"
            f"ABSOLUTE PATH: {reference.absolute()}"
        )
        self.execute_args(args=["-c", str(self.config_file)], expected_exception=expected_exception)


class TestFileCreation(BaseExceptionsTests):
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
