# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import os
import locale
import logging
import sys
from collections import Mapping, defaultdict

__all__ = [
    'init'
]


class BaseFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, include_timestamp=True):
        if include_timestamp:
            FORMAT = '%(customlevelname)s %(asctime)s: ' \
                     '%(name)s:%(lineno)d: ' \
                     '%(message)s'
        else:
            FORMAT = '%(customlevelname)s: ' \
                     '%(name)s:%(lineno)d: ' \
                     '%(message)s'

        super(BaseFormatter, self).__init__(fmt=FORMAT, datefmt=datefmt)

    def format(self, record):
        customlevel = self._get_levelname(record.levelname)
        record.__dict__['customlevelname'] = customlevel
        # format multiline messages 'nicely' to make it clear they are together
        # record.msg = record.msg.replace('\n', '\n  | ')
        if not isinstance(record.msg, str):
            record.msg = str(record.msg)

        record.msg = record.msg.replace('\n', '\n  | ')

        return super(BaseFormatter, self).format(record)

    def formatException(self, ei):
        ''' prefix traceback info for better representation '''
        # .formatException returns a bytestring in py2 and unicode in py3
        # since .format will handle unicode conversion,
        # str() calls are used to normalize formatting string
        s = super(BaseFormatter, self).formatException(ei)
        # fancy format traceback
        s = str('\n').join(str('  | ') + line for line in s.splitlines())
        # separate the traceback from the preceding lines
        s = str('  |___\n{}').format(s)
        return s

    def _get_levelname(self, name):
        ''' NOOP: overridden by subclasses '''
        return name


class ANSIFormatter(BaseFormatter):
    
    ANSI_CODES = {
        'red': '\033[1;31m',
        'yellow': '\033[1;33m',
        'cyan': '\033[1;36m',
        'green': '\033[1;32m',
        'white': '\033[1;37m',
        'bgred': '\033[1;41m',
        'bggrey': '\033[1;100m',
        'reset': '\033[0;m',
    }

    LEVEL_COLORS = {
        'INFO': 'cyan',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bgred',
        'DEBUG': 'bggrey'}

    @staticmethod
    def colorize(color, text):
        """ """
        if not supports_color():
            return text

        color = ANSIFormatter.ANSI_CODES[color]
        fmt = '{0}{1}{2}'
        return fmt.format(color, text, ANSIFormatter.ANSI_CODES['reset'])

    def _get_levelname(self, name):
        color = self.ANSI_CODES[self.LEVEL_COLORS.get(name, 'white')]
        fmt = '{0}{1}{2}'
        return fmt.format(color, name, self.ANSI_CODES['reset'])


class TextFormatter(BaseFormatter):
    """
    Convert a `logging.LogRecord' object into text.
    """
    pass


class LimitFilter(logging.Filter):
    """
    Remove duplicates records, and limit the number of records in the same
    group.

    Groups are specified by the message to use when the number of records in
    the same group hit the limit.
    E.g.: log.warning(('43 is not the answer', 'More erroneous answers'))
    """

    _ignore = set()
    _raised_messages = set()
    _threshold = 5
    _group_count = defaultdict(int)

    def filter(self, record):
        # don't limit log messages for anything above "warning"
        if record.levelno > logging.WARN:
            return True

        # extract group
        group = record.__dict__.get('limit_msg', None)
        group_args = record.__dict__.get('limit_args', ())

        # ignore record if it was already raised
        message_key = (record.levelno, record.getMessage())
        if message_key in self._raised_messages:
            return False
        else:
            self._raised_messages.add(message_key)

        # ignore LOG_FILTER records by templates when "debug" isn't enabled
        logger_level = logging.getLogger().getEffectiveLevel()
        if logger_level > logging.DEBUG:
            ignore_key = (record.levelno, record.msg)
            if ignore_key in self._ignore:
                return False

        # check if we went over threshold
        if group:
            key = (record.levelno, group)
            self._group_count[key] += 1
            if self._group_count[key] == self._threshold:
                record.msg = group
                record.args = group_args
            elif self._group_count[key] > self._threshold:
                return False
        return True


class SafeLogger(logging.Logger):
    """
    Base Logger which properly encodes Exceptions in Py2
    """
    _exc_encoding = locale.getpreferredencoding()

    def _log(self, level, msg, args, exc_info=None, extra=None):
        # if the only argument is a Mapping, Logger uses that for formatting
        # format values for that case
        if args and len(args) == 1 and isinstance(args[0], Mapping):
            args = ({k: self._decode_arg(v) for k, v in args[0].items()},)
        # otherwise, format each arg
        else:
            args = tuple(self._decode_arg(arg) for arg in args)
        super(SafeLogger, self)._log(
            level, msg, args, exc_info=exc_info, extra=extra)

    def _decode_arg(self, arg):
        """
        properly decode an arg for Py2 if it's Exception


        localized systems have errors in native language if locale is set
        so convert the message to unicode with the correct encoding
        """
        if isinstance(arg, Exception):
            text = str('%s: %s') % (arg.__class__.__name__, arg)
            return text
        else:
            return arg


class LimitLogger(SafeLogger):
    """
    A logger which adds LimitFilter automatically
    """

    limit_filter = LimitFilter()

    def __init__(self, *args, **kwargs):
        super(LimitLogger, self).__init__(*args, **kwargs)
        self.enable_filter()

    def disable_filter(self):
        self.removeFilter(LimitLogger.limit_filter)

    def enable_filter(self):
        self.addFilter(LimitLogger.limit_filter)


class FatalLogger(LimitLogger):
    warnings_fatal = False
    errors_fatal = False

    def warning(self, *args, **kwargs):
        super(FatalLogger, self).warning(*args, **kwargs)
        if FatalLogger.warnings_fatal:
            raise RuntimeError('Warning encountered')

    def error(self, *args, **kwargs):
        super(FatalLogger, self).error(*args, **kwargs)
        if FatalLogger.errors_fatal:
            raise RuntimeError('Error encountered')

# logging.setLoggerClass(FatalLogger)
logging.setLoggerClass(logging.Logger)


def supports_color():
    """
    Returns True if the running system's terminal supports color,
    and False otherwise.

    from django.core.management.color
    """
    plat = sys.platform
    supported_platform = plat not in ['Pocket PC', 'win32']

    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

    if not supported_platform or not is_a_tty:
        return False
    return True


def get_formatter(include_timestamp=True):
    if supports_color():
        return ANSIFormatter(include_timestamp=include_timestamp)
    else:
        return TextFormatter(include_timestamp=include_timestamp)


def init(level=None,
         fatal='',
         handler=logging.StreamHandler(),
         name=None,
         include_timestamp=False):

    FatalLogger.warnings_fatal = fatal.startswith('warning')
    FatalLogger.errors_fatal = bool(fatal)

    logger = logging.getLogger(name)

    handler.setFormatter(get_formatter(include_timestamp))
    logger.addHandler(handler)

    if level:
        logger.setLevel(level)


def log_warnings():
    import warnings
    logging.captureWarnings(True)
    warnings.simplefilter("default", DeprecationWarning)
    init(logging.DEBUG, name='py.warnings')


if __name__ == '__main__':
    init(level=logging.DEBUG)

    root_logger = logging.getLogger()
    root_logger.debug('debug')
    root_logger.info('info')
    root_logger.warning('warning')
    root_logger.error('error')
    root_logger.critical('critical')
