#
import logging
from test.base import TestBase

LOG = logging.getLogger(__name__)


class TestAppBase(TestBase):

    def test_app_base(self):
        """ """
        from addict import Dict
        assert isinstance(self.app.conf, Dict)

    def test_redis(self):
        from {{cookiecutter.package_name}}.lib.redis import Redis

        with Redis(force_mock=True) as redis:
            redis.set('key', 'value')
            val = redis.get('key').decode('utf-8')
            assert val == 'value'
