#!/usr/bin/env python3
"""
doc
"""
import pathlib
import unittest

from cushead.generator import images
from tests import base_tests


class TestPackages(base_tests.BaseTests):
    """
    doc
    """

    def test_cushead_generator_images(self) -> None:
        """
        doc
        """
        self.assertIsNone(images.resize_image(image=None, width=0, height=0))
        self.assertIsNone(images.remove_transparency(image=None, background_color=""))
        self.assertEqual(images.read_image_bytes(image=None), b"")

    def test_tests(self) -> None:
        """
        doc
        """
        with self.assertRaises(Exception) as exception:
            with self.assertNotRaises(Exception):
                raise Exception
        self.assertEqual(str(exception.exception), "Exception raised")

if __name__ == "__main__":
    unittest.main()
