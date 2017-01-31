#
import sys
import yaml
import logging
import argparse
from os import path
from addict import Dict

from .log import init
from .lib.singleton import Singleton


LOG = logging.getLogger(__name__)


class App(object, metaclass=Singleton):
    
    CONF_FORMAT = 'ini'

    def __init__(self):
        self._args = None
        self._config = None

    @property
    def args(self):
        if self._args:
            return self._args
        
        if self.CONF_FORMAT == 'yaml':
            default_conf = 'config.yaml'
        elif self.CONF_FORMAT == 'ini':
            default_conf = 'config.ini'

        parser = argparse.ArgumentParser()
        parser.add_argument('--conf', default=default_conf)
        parser.add_argument('--log-level', default='INFO')
        parser.add_argument('--test-mode', default=False, action='store_true')
        self._args = parser.parse_args()
        return self._args

    @property
    def config(self):
        """
        :rtype: dict
        """
        if self._config:
            return self._config

        file = self.args.conf
        LOG.info('Looking for %s' % file)

        # search each directory going up one dir at a time
        dirs = path.split(path.abspath(__file__))
        dirs = path.split(dirs[0])
        while dirs:
            if dirs[0] == '/' and not dirs[1]:
                break

            fpath = '/'.join(dirs) + '/' + file
            dirs = path.split(dirs[0])

            try:
                if self.CONF_FORMAT == 'yaml':
                    with open(fpath) as f:
                        config = yaml.load(f)
                        self._config = Dict(config)
                        LOG.info('Config %s loaded' % fpath)
                        break
                elif self.CONF_FORMAT == 'ini':
                    self._config = configparser.ConfigParser(
                        allow_no_value=True
                    )

                    self._config.read(self.args.conf)
            except (NotADirectoryError, FileNotFoundError):
                continue
            except Exception as e:
                LOG.exception(e)
                exit(-1)

        return self._config

    def run(self):
        """ application entry point """
        init(self.args.log_level)

        LOG.info(self.args)
        LOG.info(self.config)
        

def main():
    a = App()
    a.run()
