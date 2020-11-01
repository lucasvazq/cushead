#!/usr/bin/env python3
"""
Test the setup.
"""
import contextlib
import io
import sys
import unittest
from unittest.mock import patch

from tests import base_tests


class TestSetup(base_tests.BaseTests):
    """
    Main setup test class.
    """

    def test_setup(self) -> None:
        """
        Test the setup with arguments.
        """
        with self.assertNotRaises(Exception):
            with io.StringIO() as buffer, contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                with patch.object(sys, "argv", ["sdist", "bdist_wheel"]):
                    import setup
                with patch.object(sys, "argv", ["install"]):
                    import setup


if __name__ == "__main__":
    unittest.main()
