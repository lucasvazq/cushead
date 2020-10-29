"""
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
from cushead.console import arguments
from cushead.console import console


class _AssertNotRaisesContext(case._AssertRaisesContext):
    """
    doc
    """

    def __exit__(self, exc_type, exc_value, tb) -> True:
        """
        doc

        Args:
            exe_type: Exception class
            exc_value: Exception value
            tb: traceback
        """
        if exc_type is not None:
            self._raiseFailure(f"{self.expected.__name__} raised")
        return True


class BaseTests(unittest.TestCase):
    """
    doc
    """

    def __init__(self, *args, **kwargs):
        """
        doc
        """
        super().__init__(*args, **kwargs)
        self.base_folder = pathlib.Path(__file__).parent
        self.templates_folder = self.base_folder / "templates"
        self.output_folder = self.base_folder / "output"
        self.config_file = self.output_folder / "config.json"
        self.usage = arguments.setup_parser().usage

    def write_config_file(self) -> None:
        self.config_file.write_text(json.dumps(self.config))

    def execute_args(self, *, args: List[str], expected_exception: Optional[str] = None) -> None:
        """
        Run the console with the given arguments.

        Args:
            args: the arguments.
            exception_expected: an expected exception message.
        """
        if expected_exception is not None:
            with self.assertRaises(SystemExit) as exception:
                self.run_package(args=args)
            self.assertIsInstance(exception.exception, SystemExit)
            self.assertEqual(str(exception.exception), (
                f"usage: {self.usage}\n"
                f"{info.PACKAGE_NAME}: error: {expected_exception}"
            ))
        else:
            self.run_package(args=args)

    @staticmethod
    def run_package(*, args: List[str]) -> None:
        """
        doc
        """
        with io.StringIO() as f, contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
            console.init(args=args)

    def setUp(self) -> None:
        """
        doc
        """
        os.makedirs(self.output_folder)
        self.execute_args(args=["-d", "-i", str(self.config_file)])
        self.config = console.get_default_config()

    def tearDown(self) -> None:
        """
        doc
        """
        shutil.rmtree(self.output_folder.absolute())

    def assertNotRaises(self, expected_exception, *args, **kwargs):
        """
        doc
        """
        context = _AssertNotRaisesContext(expected_exception, self)
        try:
            return context.handle("assertNotRaises", args, kwargs)
        finally:
            context = None
