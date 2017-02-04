#
import logging
from test.base import TestBase

LOG = logging.getLogger(__name__)


class TestAppBase(TestBase):

    def test_app_base(self):
        """ """
        from addict import Dict
        assert isinstance(self.app.conf, Dict)


