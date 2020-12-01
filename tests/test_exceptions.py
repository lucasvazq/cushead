#!/usr/bin/env python3
"""
Test exceptions.
"""
import os
import pathlib
import shutil
import unittest

from tests import base_tests


class TestArgs(base_tests.BaseTests):
    """
    Test exceptions related to arguments passed to the CLI.
    """

    def test_invalid_args(self) -> None:
        """
        Test invalid arguments.
        """
        # Miss a required argument.
        self.execute_cli(
            args=[""],
            expected_exception=
            "Missing a required argument. Use --config, --default or --help.",
        )

        # Invalid arguments combination.
        self.execute_cli(
            args=["-c", "-d"],
            expected_exception="Can't use -c and -d arguments together.",
        )

        # Pass optional argument without a required ones.
        self.execute_cli(
            args=["-c", "-i"],
            expected_exception="Can't use -i argument without --default.",
        )

        # Miss the file.
        self.execute_cli(
            args=["-c"],
            expected_exception="The path to the config file is missing.")
        self.execute_cli(
            args=["-d"],
            expected_exception=
            "The destination path for the default config file is missing.",
        )


class TestConfig(base_tests.BaseTests):
    """
    Test exceptions related to the config.
    """

    def test_missing_key(self) -> None:
        """
        Miss required key.
        """
        del self.config["static_url"]
        self.write_config_file()
        self.execute_cli(
            args=["-c", str(self.config_file)],
            expected_exception="Missing key: 'static_url'",
        )

    def test_invalid_data_type(self) -> None:
        """
        Invalid value type.
        """
        self.config["favicon_ico"] = 1
        expected_exception = "\n".join((
            "Key 'favicon_ico' error:",
            "Or(None, <class 'str'>) did not validate 1",
            "1 should be instance of 'str'",
        ), )
        self.write_config_file()
        self.execute_cli(args=["-c", str(self.config_file)],
                         expected_exception=expected_exception)

    def test_invalid_key(self) -> None:
        """
        The config key doesn't exist.
        """
        self.config["invalid_key"] = ""
        self.write_config_file()
        self.execute_cli(
            args=["-c", str(self.config_file)],
            expected_exception=f"Wrong key 'invalid_key' in {self.config}",
        )

    def test_color_related_keys(self) -> None:
        """
        Test the hex color verification.
        """
        exception = "The key {key} must be a hex color code. If you don't want any value on this key, set the value to null."

        self.config["main_color"] = "#ffff"
        self.write_config_file()
        self.execute_cli(
            args=["-c", str(self.config_file)],
            expected_exception=exception.format(key="main_color"),
        )

        self.tearDown()
        self.setUp()

        self.config["background_color"] = "rgba(255, 255, 255, 0)"
        self.write_config_file()
        self.execute_cli(
            args=["-c", str(self.config_file)],
            expected_exception=exception.format(key="background_color"),
        )


class TestReferences(base_tests.BaseTests):
    """
    Test exception related to path references.
    """

    def test_inexistent_file(self) -> None:
        """
        The reference doesn't exists.
        """
        reference = pathlib.Path(__file__).parent / "inexistent_file.json"
        expected_exception = "\n".join((
            f"The file ({reference}) must be a reference to a path that exists.",
            f"ABSOLUTE PATH: {reference.absolute()}",
        ), )
        self.execute_cli(args=["-c", str(reference)],
                         expected_exception=expected_exception)

    def test_config_reference_is_directory(self) -> None:
        """
        The reference is a directory but a file is expected.
        """
        expected_exception = "\n".join((
            f"The file ({self.config_folder}) must be a reference to a file.",
            f"ABSOLUTE PATH: {self.config_folder.absolute()}",
        ), )
        self.execute_cli(args=["-c", str(self.config_folder)],
                         expected_exception=expected_exception)

    def test_invalid_format(self) -> None:
        """
        The config file isn't in a valid JSON format.
        """
        self.config_file.write_text("invalid file format")
        expected_exception = "\n".join((
            f"Invalid json file format in ({self.config_file})",
            f"ABSOLUTE PATH: {self.config_file.absolute()}",
            "Exception: Expecting value: line 1 column 1 (char 0)",
        ), )
        self.execute_cli(args=["-c", str(self.config_file)],
                         expected_exception=expected_exception)

    def test_image_does_not_exists(self) -> None:
        """
        The image path doesn't exist.
        """
        reference = self.config_folder / "favicon_ico_16px.ico"
        os.remove(reference)
        expected_exception = "\n".join((
            f"favicon_ico reference ({reference}) doesn't exists.",
            f"ABSOLUTE PATH: {reference.absolute()}",
        ), )
        self.execute_cli(args=["-c", str(self.config_file)],
                         expected_exception=expected_exception)

    def test_image_reference_is_directory(self) -> None:
        """
        The image path is a directory.
        """
        reference = self.config_folder / "favicon_ico_16px.ico"
        os.remove(reference)
        os.makedirs(reference)
        expected_exception = "\n".join((
            f"favicon_ico reference ({reference}) must be a file, not a directory.",
            f"Exception: [Errno 21] Is a directory: '{reference.absolute()}'",
        ), )
        self.execute_cli(args=["-c", str(self.config_file)],
                         expected_exception=expected_exception)

    def test_image_reference_is_not_a_image_file(self) -> None:
        """
        The image path isn't an image file type.
        """
        reference = self.config_folder / "favicon_ico_16px.ico"
        reference.write_bytes(b"")
        expected_exception = "\n".join((
            f"Can't identify as image the favicon_ico reference ({reference}).",
            f"Exception: cannot identify image file '{reference.absolute()}'",
        ), )
        self.execute_cli(args=["-c", str(self.config_file)],
                         expected_exception=expected_exception)

    def test_invalid_image_format(self) -> None:
        """
        The image path has a different image type of the expected.
        """
        reference = self.config_folder / "favicon_ico_16px.ico"
        shutil.copy(self.config_folder / "favicon_png_2688px.png", reference)
        expected_exception = "\n".join((
            f"The favicon_ico reference ({reference}) has a wrong image format.",
            "Expected ICO, but received PNG.",
            f"ABSOLUTE PATH: {reference.absolute()}",
        ), )
        self.execute_cli(args=["-c", str(self.config_file)],
                         expected_exception=expected_exception)


class TestFileCreation(base_tests.BaseTests):
    """
    Test exceptions related to files creation.
    """

    def test_file_creation(self) -> None:
        """
        Can't create a file because a directory exists in the path.
        """
        reference = self.config_folder / "directory"
        os.mkdir(reference)
        self.execute_cli(args=["-d", str(reference)])


if __name__ == "__main__":
    unittest.main()
