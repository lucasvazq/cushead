#!/usr/bin/env python3
"""
doc
"""
import sys
import unittest
from unittest.mock import patch

from tests import base_tests


class TestSetup(base_tests.BaseTests):
    """
    doc
    """

    def test_setup(self) -> None:
        """
        doc
        """
        with self.assertNotRaises(Exception):
            with patch.object(sys, "argv", ["sdist", "bdist_wheel"]):
                import setup
            with patch.object(sys, "argv", ["install"]):
                import setup


if __name__ == "__main__":
    unittest.main()
