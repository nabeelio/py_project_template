#
import io
import sys
import logging
import unittest
import argparse


def all_tests():
    """
    add of the unit test suites here
    """
    suite = unittest.TestSuite()

    # Add test suites here
    from test.test_app import TestAppBase
    suite.addTests(unittest.makeSuite(TestAppBase))

    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    all_tests()
