#
import logging
from {{cookiecutter.package_name}}.app import App
from {{cookiecutter.package_name}}.lib.singleton import Singleton

LOG = logging.getLogger(__name__)


class Redis(metaclass=Singleton):

    def __init__(self, force_mock=False):
        self._redis = None
        self.force_mock = force_mock

        self.args = App().args
        self.conf = App().conf

    def __getattr__(self, item):
        return getattr(self.redis, item)

    def __enter__(self):
        """ for use as
         with Redis() as redis:
        """
        return self.redis

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def _connect(self):
        """ Connect to Redis """
        if self.force_mock or self.args.test_mode:
            LOG.info('In test mode, loading MockRedis')
            from mockredis.client import MockRedis
            return MockRedis(strict=True,
                             decode_responses=True)

        from redis import StrictRedis

        host = self.conf.general.redis
        port = self.conf.redis.port
        LOG.info('Connecting to {0}:{1}'.format(host, port))
        return StrictRedis(host=host,
                           port=port,
                           decode_responses=True)

    @property
    def redis(self):
        """
        :rtype: redis.StrictRedis
        """
        if not self._redis:
            self._redis = self._connect()

        return self._redis

    def instance(self):
        return self.redis
