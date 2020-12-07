#!/usr/bin/env python3
"""
Test different configs.
"""
import pathlib
import unittest

from tests import base_tests


class TestConfig(base_tests.BaseTests):
    """
    Main config test class.
    """

    def compare_output(self, *, template_folder_path: pathlib.Path) -> None:
        """
        Compare the expected output with the real output.

        Args:
            template_folder_path: the path, relative to the templates_folder instance attribute, that has the expected files.
        """
        template_folder = self.base_folder / "templates" / template_folder_path

        # Compare the folders structure.
        self.assertEqual(
            [str(file.relative_to(self.output_folder)) for file in self.output_folder.rglob("*")],
            [str(file.relative_to(template_folder)) for file in template_folder.rglob("*")],
        )

        # Compare the files.
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
        Test the default config.
        """
        self.execute_cli(args=["-c", str(self.config_file)])
        self.compare_output(template_folder_path=pathlib.Path("default_config"))

    def test_missing_keys(self) -> None:
        """
        Test a config without any non-required field.
        """
        self.config.clear()
        self.config["static_url"] = self.config["static_url"]
        self.write_config_file()
        self.execute_cli(args=["-c", str(self.config_file)])
        self.compare_output(template_folder_path=pathlib.Path("missing_keys"))

    def test_empty_strings(self) -> None:
        """
        Test a configuration that has all empty-string values.
        """
        for key in self.config:
            self.config[key] = ""
        self.write_config_file()
        self.execute_cli(args=["-c", str(self.config_file)])
        self.compare_output(template_folder_path=pathlib.Path("empty_strings"))

    def test_null_values(self) -> None:
        """
        Test a configuration that has all non-required values ​​null.
        """
        for key in self.config:
            if key == "static_url":
                continue
            self.config[key] = None
        self.write_config_file()
        self.execute_cli(args=["-c", str(self.config_file)])
        self.compare_output(template_folder_path=pathlib.Path("null_values"))

    def test_custom_key_values(self) -> None:
        """
        Test custom key values.
        """
        # Without background_color key.
        del self.config["background_color"]
        self.write_config_file()
        self.execute_cli(args=["-c", str(self.config_file)])
        self.compare_output(template_folder_path=pathlib.Path("custom_key_values/background_color"))

        self.tearDown()
        self.setUp()

        # Without title key.
        del self.config["title"]
        self.write_config_file()
        self.execute_cli(args=["-c", str(self.config_file)])
        self.compare_output(template_folder_path=pathlib.Path("custom_key_values/title"))

        self.tearDown()
        self.setUp()

        # Using an URL instead of a path for the static files.
        self.config["static_url"] = "https://cdn.com/instance"
        self.write_config_file()
        self.execute_cli(args=["-c", str(self.config_file)])
        self.compare_output(template_folder_path=pathlib.Path("custom_key_values/static_url"))

    def test_exmaple_config(self) -> None:
        """
        Test the example saved in docs.
        """
        self.config["google_tag_manager"] = "GTM-NGGH6LK"
        self.write_config_file()
        self.execute_cli(args=["-c", str(self.config_file)])
        self.compare_output(template_folder_path=pathlib.Path("../../docs/example/dist"))


if __name__ == "__main__":
    unittest.main()
