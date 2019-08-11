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
        main(['-file', '-preset'])

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
        main(['-file', './test/void/test.txt'])

    # index.html doesn't exists
    # Exception
    def test_6(self):
        main(['-file', './test/missing/test.txt'])

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


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestApp))
    return suite
    
unittest.TextTestRunner(verbosity=2).run(suite())