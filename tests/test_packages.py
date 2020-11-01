#!/usr/bin/env python3
"""
Test functions that can't be tested with the other tests.
"""
import pathlib
import unittest

from cushead.generator import images
from tests import base_tests


class TestPackages(base_tests.BaseTests):
    """
    Main test class of this module.
    """

    def test_cushead_generator_images(self) -> None:
        """
        Test functions of cushead.generator.images
        """
        self.assertIsNone(images.get_resized_image(image=None, width=0, height=0))
        self.assertIsNone(images.get_opaque_image(image=None, background_color=""))
        self.assertEqual(images.get_image_bytes(image=None), b"")

    def test_tests(self) -> None:
        """
        Test the test features.
        """
        with self.assertRaises(Exception) as exception:
            with self.assertNotRaises(Exception):
                raise Exception
        self.assertEqual(str(exception.exception), "Exception raised")

if __name__ == "__main__":
    unittest.main()
