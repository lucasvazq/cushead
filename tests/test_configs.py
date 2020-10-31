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

        # Check folders structure
        self.assertEqual(
            [str(file.relative_to(self.output_folder)) for file in self.output_folder.rglob("*")],
            [str(file.relative_to(template_folder)) for file in template_folder.rglob("*")]
        )

        # Compare files
        for generated_file in self.output_folder.rglob("*"):
            template_file = template_folder / str(generated_file.relative_to(self.output_folder))
            if generated_file.is_dir():
                self.assertTrue(template_file.is_dir())
            elif generated_file.suffix in (".png", ".ico"):
                self.assertEqual(generated_file.read_bytes(), template_file.read_bytes())
            else:
                self.assertEqual(generated_file.read_text(), template_file.read_text())

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
        self.compare_output("custom_config/1")

        self.set_default_config()
        self.config["static_url"] = "https://cdn.com"
        self.write_config_file()
        self.execute_args(args=["-c", str(self.config_file)])
        self.compare_output("custom_config/2")


if __name__ == "__main__":
    unittest.main()
