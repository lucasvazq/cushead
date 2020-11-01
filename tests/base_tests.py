"""
Base test class.
"""
import contextlib
import io
import json
import os
import pathlib
import shutil
import traceback
import unittest
from typing import List
from typing import Optional
from unittest import case

from cushead import info
from cushead.console import console
from cushead.console.arguments import config
from cushead.console.arguments import setup


class _AssertNotRaisesContext(case._AssertRaisesContext):
    """
    Class to use as a context that verifies that no exceptions are thrown.
    """

    def __exit__(self, exc_type, *args) -> True:
        if exc_type is not None:
            self._raiseFailure(f"{self.expected.__name__} raised")
        return True


class BaseTests(unittest.TestCase):
    """
    Base class for all tests classes.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the class and define useful attributes.
        """
        super().__init__(*args, **kwargs)
        self.base_folder = pathlib.Path(__file__).parent
        self.templates_folder = self.base_folder / "templates"
        self.config_folder = self.base_folder / "config"
        self.config_file = self.config_folder / "config.json"
        self.output_folder = self.config_folder / "output"
        self.usage = setup.setup_parser().usage

    @staticmethod
    def _execute_the_CLI_silently(*, args: List[str]) -> None:
        """
        Execute the CLI without output.

        Args:
            args: the args.
        """
        with io.StringIO() as buffer, contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
            console.init(args=args)

    def execute_the_CLI(self, *, args: List[str], expected_exception: Optional[str] = None) -> None:
        """
        Execute the CLI and check if it behaves as expected.

        Args:
            args: the arguments.
            exception_expected: the exception message, if an exception is expected.
        """
        if expected_exception is None:
            self._execute_the_CLI_silently(args=args)
        else:
            with self.assertRaises(SystemExit) as exception:
                self._execute_the_CLI_silently(args=args)
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
        self.config = config.get_default_config()

    def write_config_file(self) -> None:
        """
        Write a config file using the config instance attribute.
        """
        self.config_file.write_text(json.dumps(self.config))

    def setUp(self) -> None:
        """
        A method that is called immediately before calling the test method.

        It creates the default configuration file with images and sets the default config in the config instance attribute.
        """
        os.makedirs(self.config_folder)
        self.execute_the_CLI(args=["-d", "-i", str(self.config_file)])
        self.set_default_config()

    def tearDown(self) -> None:
        """
        A method that is called immediately after calling the test method.

        It removes all the files created by the test and setUp methods.
        """
        shutil.rmtree(self.config_folder.absolute())

    def assertNotRaises(self, expected_exception, *args, **kwargs):
        """
        Verifies that no exceptions are thrown.
        """
        context = _AssertNotRaisesContext(expected_exception, self)
        try:
            return context.handle("assertNotRaises", args, kwargs)
        finally:
            context = None
