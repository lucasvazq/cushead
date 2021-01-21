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

import setup


class TestSetup(base_tests.BaseTests):
    """
    Main setup test class.
    """

    @staticmethod
    def test_setup() -> None:
        """
        Test the setup with arguments.
        """
        # Test that no exceptions occur
        with io.StringIO() as buffer, contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
            with patch.object(sys, "argv", ["setup.py", "sdist", "bdist_wheel"]):
                setup.setup()
            with patch.object(sys, "argv", ["setup.py", "install"]):
                setup.setup()


if __name__ == "__main__":
    unittest.main()
