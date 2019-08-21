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

# The path passed with 'outputh' isn't a folder
def test_output_no_folder(self):
    with self.assertRaises(Exception) as e:
        Main(INFO, ['-file',
            './test/tests/ConfigExceptions/output_no_folder/test.txt']).run()
    self.assertRegex(str(e.exception),
        "('output' )(\(.*\))( must be referred to a folder path.)(\n.*)")
            
"""


# Success
class TestSuccess(unittest.TestCase):

    # Complete config
    @staticmethod
    def test_complete_config():
        arguments = ['-file', './test/tests/Success/complete_config/test.txt']
        Main(INFO, arguments).run()

    # -preset
    @staticmethod
    def test_preset():
        pass
        arguments = ['-preset', './test/tests/Success/preset/test.txt']
        Main(INFO, arguments).run()


def suite_setup():
    suite = unittest.TestSuite()
    test_classes = [TestSuccess]
    for test_class in test_classes:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_class))
    return suite


with contextlib.redirect_stdout(io.StringIO()) as stdout:
    unittest.TextTestRunner(verbosity=3).run(suite_setup())
