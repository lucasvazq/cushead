#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock
import argparse
from cushead import main


class TestApp(unittest.TestCase):
    # no arguments
    # Exception
    def test_1(self):
        main([])

    # -file and -preset together
    # Exception
    def test_2(self):
        main(['-file', './test/together/test.txt', '-preset', './test/together/foo.bar'])

    # argument passed with -file doesn't exists
    # Exception
    def test_3(self):
        main(['-file', 'foo.bar'])

    # correct -file usage
    # Success
    def test_4(self):
        main(['-file', './test/correct/test.txt'])

    # void index.html
    # Success
    def test_5(self):
        main(['-file', './test/void_index/test.txt'])

    # index.html doesn't exists
    # Exception
    def test_6(self):
        main(['-file', './test/miss_index/test.txt'])

    # all optional parameters
    # Success
    def test_7(self):
        main(['-file', './test/options/test.txt',
            '--exclude-comment',
            '--exclude-html',
            '--exclude-config',
            '--exclude-seo',
            '--exclude-opengraph',
            '--exclude-facebook',
            '--exclude-twitter',
            '--exclude-opensearch',
            '--exclude-author'
            ])

    # correct -preset usage
    # Success
    def test_8(self):
        main(['-preset', './test/foo.bar'])

    # file passed with -file doesn't have path key-value pair
    # Exception
    def test_9(self):
        main(['-file', './test/miss_path/test.txt'])

    # file passed with -file only have path key-value pair
    # Success
    def test_10(self):
        main(['-file', './test/only_path/test.txt'])

    # file passed with -file are void
    # Exception
    def test_11(self):
        main(['-file', './test/miss_value_preset/test.txt'])

    # missing some key-value pairs
    # color, title, preview, description
    # Success
    def test_12(self):
        main(['-file', './test/miss_special/test.txt'])

    # void some values in key pairs
    # color, title, preview, description
    # Success
    def test_13(self):
        main(['-file', './test/void_special/test.txt'])

    # void all values except path
    # Success
    def test_14(self):
        main(['-file', './test/void_except_path/test.txt'])

    # void all values
    # Exception
    def test_15(self):
        main(['-file', './test/void_preset/test.txt'])

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestApp))
    return suite

unittest.TextTestRunner(verbosity=2).run(suite())