#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contextlib
import io
import os
import sys
import unittest

try:
    sys.path.insert(1, os.path.join(sys.path[0], '..'))
except Exception as e:
    print(e)

from src.info import get_info
from src.main import Main


INFO = get_info()

"""

    def test_exit(self):
        with self.assertRaises(SystemExit) as ex:
            Main(INFO, [])
        self.assertRegex(str(ex.exception), "WASAAA")
            
"""


# Success
class TestSuccess(unittest.TestCase):

    # Complete config
    @staticmethod
    def test_complete_config():
        arguments = ['-file',
                     './test/tests/Success/complete_config/config.json']
        Main(INFO, arguments).run()

    # -preset
    @staticmethod
    def test_preset():
        arguments = ['-preset',
                     './test/tests/Success/preset/config.json']
        Main(INFO, arguments).run()


def suite_setup():
    suite = unittest.TestSuite()
    test_classes = [TestSuccess]
    for test_class in test_classes:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_class))
    return suite


unittest.TextTestRunner().run(suite_setup())
