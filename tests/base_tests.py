"""
Base test class.
"""
import contextlib
import io
import json
import os
import pathlib
import shutil
import unittest
from typing import Any, List, Optional

from cushead import info
from cushead.console import console
from cushead.console.arguments import config, setup


class BaseTests(unittest.TestCase):
    """
    Base class for all tests classes.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        """
        Initialize the class and define useful attributes.
        """
        super().__init__(*args, **kwargs)
        self.maxDiff = None
        self.base_folder = pathlib.Path(__file__).parent
        self.config_folder = self.base_folder / "config"
        self.config_file = self.config_folder / "config.json"
        self.output_folder = self.config_folder / "output"
        self.usage = setup.get_parser().usage

    @staticmethod
    def _execute_cli_silently(*, args: List[str]) -> None:
        """
        Execute the CLI without output.

        Args:
            args: the args.
        """
        with io.StringIO() as buffer, contextlib.redirect_stdout(
            buffer
        ), contextlib.redirect_stderr(buffer):
            console.init(args=args)

    def execute_cli(
        self, *, args: List[str], expected_exception: Optional[str] = None
    ) -> None:
        """
        Execute the CLI and check if it behaves as expected.

        Args:
            args: the arguments.
            expected_exception: the exception message, if an exception is expected.
        """
        if expected_exception is None:
            self._execute_cli_silently(args=args)
        else:
            with self.assertRaises(SystemExit) as exception:
                self._execute_cli_silently(args=args)
            self.assertIsInstance(exception.exception, SystemExit)
            self.assertEqual(
                str(exception.exception),
                "\n".join(
                    (
                        f"usage: {self.usage}",
                        f"{info.PACKAGE_NAME}: error: {expected_exception}",
                    ),
                ),
            )

    def set_default_config(self) -> None:
        """
        Set the default config to the config instance attribute.
        """
        self.config = dict(config.get_default_config())

    def write_config_file(self) -> None:
        """
        Write a config file using the config instance attribute.
        """
        self.config_file.write_text(json.dumps(self.config))

    def remove_output_folder(self) -> None:
        """
        Remove the output folder.
        """
        shutil.rmtree(self.config_folder.absolute())

    def setUp(self) -> None:
        """
        Create the default configuration file with images and set the default config in the config instance attribute.
        """
        os.makedirs(self.config_folder)
        self.execute_cli(args=["-d", "-i", str(self.config_file)])
        self.set_default_config()

    def tearDown(self) -> None:
        """
        Remove all the files created by the tests and by the setUp method.
        """
        self.remove_output_folder()
