#
import unittest

from {{ cookiecutter.package_name }}.app import App

class TestBase(unittest.TestCase):
    def setUp(self):
        super(TestBase, self).__init__()
        self.app = App()
