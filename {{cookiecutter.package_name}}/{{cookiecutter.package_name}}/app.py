#
import os
import sys
import yaml
import logging
import argparse
from addict import Dict

from {{cookiecutter.package_name}} import log
from {{cookiecutter.package_name}}.lib.singleton import Singleton


LOG = logging.getLogger(__name__)


class App(object, metaclass=Singleton):

    def __init__(self, args=None):
        """ """
        self._args = None
        self._config = None
        self._conf_format = 'ini'
        self._passed_args = args or {}

        log.init(self.args.log_level)
        for logger, log_level in self.conf.logging.items():
            tmp_logger = logging.getLogger(logger)
            tmp_logger.setLevel(getattr(logging, log_level))

    @property
    def args(self):
        if self._args:
            return self._args

        if self._conf_format == 'yaml':
            default_conf = 'config.yaml'
        elif self._conf_format == 'ini':
            default_conf = 'config.ini'

        parser = argparse.ArgumentParser()

        parser.add_argument('--conf', default=default_conf)
        parser.add_argument('--log-level', default='INFO')
        parser.add_argument('--test-mode', default=False,
                            action='store_true')

        self._args = parser.parse_args()

        if self._passed_args:
            for key, value in self._passed_args.items():
                setattr(self._args, key, value)

        return self._args

    @property
    def conf(self):
        """
        :rtype: dict
        """
        if self._config:
            return self._config

        config_text = ''
        file = self.args.conf
        LOG.info('Looking for %s' % file)

        # search each directory going up one dir at a time
        dirs = os.path.split(os.path.abspath(__file__))
        dirs = os.path.split(dirs[0])

        while dirs:
            if dirs[0] == '/' and not dirs[1]:
                break

            fpath = '/'.join(dirs) + '/' + file
            dirs = os.path.split(dirs[0])

            try:
                if not os.path.exists(fpath):
                    continue

                with open(fpath, 'r') as f:
                    config_text = f.read()

                break
            except (NotADirectoryError, FileNotFoundError):
                continue
            except Exception as e:
                LOG.exception(e)
                exit(-1)

        LOG.info('Config loaded from %s' % fpath)

        # look for ${HOME}, etc and expand it
        config_text = os.path.expandvars(config_text)

        if self.CONF_FORMAT == 'yaml':
            config = yaml.load(config_text)
            self._config = Dict(config)
        elif self.CONF_FORMAT == 'ini':
            conf = configparser.ConfigParser(
                allow_no_value=True
            )

            conf.read_string(config_text)
            self._config = Dict(conf._sections)

        return self._config

    def run(self):
        """ application entry point """
        LOG.info(self.args)
        LOG.info(self.conf)


def main():
    a = App()
    a.run()
