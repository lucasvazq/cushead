#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from contextlib import redirect_stdout
from io import StringIO

from _info import get_info
from src.main import Main


INFO = get_info()


# Exceptions
class TestArgumentsException(unittest.TestCase):

    # No arguments
    def test_no_arguments(self):
        with self.assertRaises(Exception) as e:
            Main(INFO, []).run()
        self.assertEqual("Miss arguments. Use -preset or -file", str(e.exception))

    # -file and -preset together
    def test_two_arguments(self):
        with self.assertRaises(Exception) as e:
            Main(INFO, ['-file', 'foo/bar', '-preset', 'foo/bar']).run()
        self.assertEqual("Can't use -preset and -file arguments together.", str(e.exception))

    # The path passed with 'html_file' doesn't exists
    def test_file_doesnt_exists(self):
        with self.assertRaises(Exception) as e:
            Main(INFO, ['-file', 'foo/bar']).run()
        self.assertRegex(str(e.exception),
            "(-file )(\(.*\))( must be referred to a file path that exists.)(\n.*)")

    # The path passed with 'html_file' isn't a file
    def test_file_no_file(self):
        with self.assertRaises(Exception) as e:
            Main(INFO, ['-file', './test']).run()
        self.assertRegex(str(e.exception),
            "(-file )(\(.*\))( must be referred to a file path.)(\n.*)")


# Exceptions
class TestConfigExceptions(unittest.TestCase):

    # Miss 'config' variable in config file
    def test_miss_config_variable(self):
        with self.assertRaises(Exception) as e:
            Main(INFO, ['-file',
                './test/ConfigExceptions/miss_config_variable/test.txt']).run()
        self.assertRegex(str(e.exception),
            "(Can't found 'config' variable in )(\(.*\))(\n.*)")

    # Void 'icon_png' key value
    def test_void_icon_png(self):
        with self.assertRaises(Exception) as e:
            Main(INFO, ['-file', './test/ConfigExceptions/void_icon_png/test.txt']).run()
        self.assertEqual("'icon_png' key value can't be void.", str(e.exception))

    # Path passed with 'icon_png' doesn't exists
    def test_icon_png_doesnt_exists(self):
        with self.assertRaises(Exception) as e:
            Main(INFO, ['-file',
                './test/ConfigExceptions/icon_png_doesnt_exists/test.txt']).run()
        self.assertRegex(str(e.exception),
            "('icon_png' key )(\(.*\))( must be referred to a file path that exists.)(\n.*)")

    # Miss 'html_file' key
    def test_miss_html_file(self):
        with self.assertRaises(Exception) as e:
            Main(INFO, ['-file', './test/ConfigExceptions/miss_html_file/test.txt']).run()
        self.assertEqual("Miss 'html_file' key and it's required.", str(e.exception))

    # Void 'html_file' key value
    def test_void_html_file(self):
        with self.assertRaises(Exception) as e:
            Main(INFO, ['-file', './test/ConfigExceptions/void_html_file/test.txt']).run()
        self.assertEqual("'html_file' value can't be void.", str(e.exception))

    # The path passed with 'html_file' doesn't exists
    def test_html_file_doesnt_exists(self):
        with self.assertRaises(Exception) as e:
            Main(INFO, ['-file',
                './test/ConfigExceptions/html_file_doesnt_exists/test.txt']).run()
        self.assertRegex(str(e.exception),
            "('html_file' )(\(.*\))( must be referred to a file path that exists.)(\n.*)")

    # The path passed with 'html_file' isn't a file
    def test_html_file_no_file(self):
        with self.assertRaises(Exception) as e:
            Main(INFO, ['-file', './test/ConfigExceptions/html_file_no_file/test.txt']).run()
        self.assertRegex(str(e.exception),
            "('html_file' )(\(.*\))( must be referred to a file path.)(\n.*)")

    # Miss 'output' key
    def test_miss_output(self):
        with self.assertRaises(Exception) as e:
            Main(INFO, ['-file', './test/ConfigExceptions/miss_output/test.txt']).run()
        self.assertEqual("Miss 'output' key and it's required.", str(e.exception))

    # The path passed with 'output' doesn't exists
    def test_output_doesnt_exists(self):
        with self.assertRaises(Exception) as e:
            Main(INFO, ['-file',
                './test/ConfigExceptions/output_doesnt_exists/test.txt']).run()
        self.assertRegex(str(e.exception),
            "('output' )(\(.*\))( must be referred to a folder path that exists.)(\n.*)")

    # The path passed with 'outputh' isn't a folder
    def test_output_no_folder(self):
        with self.assertRaises(Exception) as e:
            Main(INFO, ['-file',
                './test/ConfigExceptions/output_no_folder/test.txt']).run()
        self.assertRegex(str(e.exception),
            "('output' )(\(.*\))( must be referred to a folder path.)(\n.*)")

    # Miss 'static_url' key
    def test_miss_static_url(self):
        with self.assertRaises(Exception) as e:
            Main(INFO, ['-file', './test/ConfigExceptions/miss_static_url/test.txt']).run()
        self.assertEqual("Miss 'static_url' key and it's required.", str(e.exception))

# Success
class TestSuccess(unittest.TestCase):

    # Complete config
    @staticmethod
    def test_complete_config():
        Main(INFO, ['-file', './test/Success/complete_config/test.txt']).run()

    # Void config
    @staticmethod
    def test_void_config():
        Main(INFO, ['-file', './test/Success/void_config/test.txt']).run()

    # Void *.html file
    @staticmethod
    def test_void_html_FILE():
        Main(INFO, ['-file', './test/Success/void_html_FILE/test.txt']).run()

    # -preset
    @staticmethod
    def test_preset():
        Main(INFO, ['-preset', './test/Success/test.txt']).run()


# Success
class TestSpecialConfigSuccess(unittest.TestCase):

    # Miss 'icon', 'mask_icon', 'browserconfig', 'manifest' and 'opensearch'
    @staticmethod
    def test_miss_1():
        Main(INFO, ['-file', './test/SpecialConfigSuccess/miss_1/test.txt']).run()

    # Miss 'title', 'description', 'dir', 'start_url', 'orientation', 'color',
    # 'locale', 'scope', 'display', 'platform' and 'applications'
    @staticmethod
    def test_miss_2():
        Main(INFO, ['-file', './test/SpecialConfigSuccess/miss_2/test.txt']).run()

    # Miss 'url'
    @staticmethod
    def test_miss_url():
        Main(INFO, ['-file', './test/SpecialConfigSuccess/miss_url/test.txt']).run()

    # Miss 'sitemap'
    @staticmethod
    def test_miss_sitemap():
        Main(INFO, ['-file', './test/SpecialConfigSuccess/miss_sitemap/test.txt']).run()


def suite():
    suite = unittest.TestSuite()
    test_classes = [TestArgumentsException, TestConfigExceptions, TestSuccess,
        TestSpecialConfigSuccess]
    for test_class in test_classes:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_class))
    return suite


with redirect_stdout(StringIO()) as stdout:
    unittest.TextTestRunner(verbosity=3).run(suite())
