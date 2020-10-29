#!/usr/bin/env python3
"""
doc
"""
import pathlib
import unittest

from tests import base_tests


class TestConfig(base_tests.BaseTests):
    """
    doc
    """

    def compare_output(self, template_folder_name: str) -> None:
        """
        doc
        """
        template_folder = self.templates_folder / template_folder_name
        for file in (self.output_folder / "output").rglob("*"):
            file_path = template_folder / str(file.relative_to(self.output_folder / "output"))

            if file.is_dir():
                self.assertTrue(file_path.is_dir())
                continue

            self.assertEqual(file.read_bytes(), file_path.read_bytes())

    def test_default_config(self) -> None:
        """
        doc
        """
        self.execute_args(args=["-c", str(self.config_file)])
        self.compare_output("default_config")

    def test_missing_keys(self) -> None:
        """
        doc
        """
        self.config = {'static_url': self.config['static_url']}
        self.write_config_file()
        self.execute_args(args=["-c", str(self.config_file)])
        self.compare_output("missing_keys")

    def test_empty_strings(self) -> None:
        """
        doc
        """
        for key in self.config:
            self.config[key] = ""
        self.write_config_file()
        self.execute_args(args=["-c", str(self.config_file)])
        self.compare_output("empty_strings")

    def test_null_values(self) -> None:
        """
        doc
        """
        for key in self.config:
            if key == "static_url":
                continue
            self.config[key] = None
        self.write_config_file()
        self.execute_args(args=["-c", str(self.config_file)])
        self.compare_output("null_values")

    def test_custom_config(self) -> None:
        """
        doc
        """
        del self.config["background_color"]
        self.write_config_file()
        self.execute_args(args=["-c", str(self.config_file)])
        self.compare_output("custom_config")


if __name__ == "__main__":
    unittest.main()
