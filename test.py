#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from src.main import Main


# Exceptions
class TestArgumentsException(unittest.TestCase):

    # No arguments
    @classmethod
    def test_no_arguments(self):
        Main([]).run()

    # -file and -preset together
    @classmethod
    def test_two_arguments(self):
        Main(['-file', 'foo/bar', '-preset', 'foo/bar']).run()

    # The path passed with 'html_file' doesn't exists
    @classmethod
    def test_file_doesnt_exists(self):
        Main(['-file', 'foo/bar']).run()

    # The path passed with 'html_file' isn't a file
    @classmethod
    def test_file_no_file(self):
        Main(['-file', './test']).run()


# Exceptions
class TestConfigExceptions(unittest.TestCase):

    # Miss 'config' variable in config file
    @classmethod
    def test_miss_config_variable(self):
        Main(['-file', './test/ConfigExceptions/miss_config_variable/test.txt']).run()

    # Void 'icon_png' key value
    @classmethod
    def test_void_icon_png(self):
        Main(['-file', './test/ConfigExceptions/void_icon_png/test.txt']).run()

    # Path passed with 'icon_png' doesn't exists
    @classmethod
    def test_icon_png_doesnt_exists(self):
        Main(['-file','./test/ConfigExceptions/icon_png_doesnt_exists/test.txt']
            ).run()

    # Miss 'html_file' key
    @classmethod
    def test_miss_html_file(self):
        Main(['-file', './test/ConfigExceptions/miss_html_file/test.txt']).run()

    # Void 'html_file' key value
    @classmethod
    def test_void_html_file(self):
        Main(['-file', './test/ConfigExceptions/void_html_file/test.txt']).run()

    # The path passed with 'html_file' doesn't exists
    @classmethod
    def test_html_file_doesnt_exists(self):
        Main(['-file', './test/ConfigExceptions/html_file_doesnt_exists/test.txt']
            ).run()

    # The path passed with 'html_file' isn't a file
    @classmethod
    def test_html_file_no_file(self):
        Main(['-file', './test/ConfigExceptions/html_file_no_file/test.txt']).run()

    # Miss 'output' key
    @classmethod
    def test_miss_output(self):
        Main(['-file', './test/ConfigExceptions/miss_output/test.txt']).run()

    # The path passed with 'output' doesn't exists
    @classmethod
    def test_output_doesnt_exists(self):
        Main(['-file', './test/ConfigExceptions/output_doesnt_exists/test.txt']).run()

    # The path passed with 'outputh' isn't a folder
    @classmethod
    def test_output_no_folder(self):
        Main(['-file', './test/ConfigExceptions/output_no_folder/test.txt']).run()

    # Miss 'static_url' key
    @classmethod
    def test_miss_static_url(self):
        Main(['-file', './test/ConfigExceptions/miss_static_url/test.txt']).run()


# Success
class TestSuccess(unittest.TestCase):

    # Complete config
    @classmethod
    def test_complete_config(self):
        Main(['-file', './test/Success/complete_config/test.txt']).run()

    # Void config
    @classmethod
    def test_void_config(self):
        Main(['-file', './test/Success/void_config/test.txt']).run()

    # Void *.html file
    @classmethod
    def test_void_html_FILE(self):
        Main(['-file', './test/Success/void_html_FILE/test.txt']).run()

    # -preset
    @classmethod
    def test_preset(self):
        Main(['-preset', './test/Success/test.txt']).run()


# Success
class TestSpecialConfigSuccess(unittest.TestCase):

    # Miss 'icon', 'mask_icon', 'browserconfig', 'manifest' and 'opensearch'
    @classmethod
    def test_miss_1(self):
        Main(['-file', './test/SpecialConfigSuccess/miss_1/test.txt']).run()

    # Miss 'title', 'description', 'dir', 'start_url', 'orientation', 'color',
    # 'locale', 'scope', 'display', 'platform' and 'applications'
    @classmethod
    def test_miss_2(self):
        Main(['-file', './test/SpecialConfigSuccess/miss_2/test.txt']).run()

    # Miss 'url'
    @classmethod
    def test_miss_url(self):
        Main(['-file', './test/SpecialConfigSuccess/miss_url/test.txt']).run()

    # Miss 'sitemap'
    @classmethod
    def test_miss_sitemap(self):
        Main(['-file', './test/SpecialConfigSuccess/miss_sitemap/test.txt']).run()


def suite():
    suite = unittest.TestSuite()
    test_classes = [TestArgumentsException, TestConfigExceptions, TestSuccess,
        TestSpecialConfigSuccess]
    for test_class in test_classes:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_class))
    return suite
    pass


unittest.TextTestRunner(verbosity=3).run(suite())
