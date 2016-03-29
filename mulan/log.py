# -*- coding:utf-8 -*-
import os, time, threading
import logging
import logging.handlers

try:
    import codecs
except ImportError:
    codecs = None

import raven

"""
例程：
from somelib import Logger

# 默认log存放目录,需要在程序入口调用才能生效,可省略
logger.log_dir = "./app"
# log文件名前缀,需要在程序入口调用才能生效,可省略
logger.log_name = "test_log"

logger = Logger()
logger.debug('debug')
logger.warn('tr-warn')
logger.info('ds-info')
logger.error('ss-error')

"""
__author__ = 'simi'

log_dir = "log"
log_name = "mulan"

_logger_init_lock = threading.Lock()


class MulanTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """
    自己定义的TimedRotatingFileHandler
    """

    def __init__(self, log_dir, file_name_prefix):
        self.log_dir = log_dir
        self.file_name_prefix = file_name_prefix

        self._mkdirs()

        self.base_filename = "%s.%s.log" % (os.path.join(self.log_dir, file_name_prefix), time.strftime("%Y%m%d"))

        logging.handlers.TimedRotatingFileHandler.__init__(self,
                                                           self.base_filename,
                                                           when='midnight', interval=1,
                                                           backupCount=0, encoding=None)

    def doRollover(self):
        self.stream.close()
        # get the time that this sequence started at and make it a TimeTuple
        t = self.rolloverAt - self.interval
        # time_tuple = time.localtime(t)
        self.base_filename = "%s.%s.log" % (os.path.join(self.log_dir, self.file_name_prefix),
                                           time.strftime("%Y%m%d"))
        if self.encoding:
            self.stream = codecs.open(self.base_filename, 'a', self.encoding)
        else:
            self.stream = open(self.base_filename, 'a')
        self.rolloverAt = self.rolloverAt + self.interval

    def _mkdirs(self):
        if not os.path.exists(self.log_dir):
            try:
                os.makedirs(self.log_dir)
            except Exception, e:
                print str(e)


class Logger(object):
    __instance = None
    log_dir = ''
    log_name = ''
    is_debug = True
    is_info = True
    is_warn = True
    is_error = True
    sentry = None

    logger_formatter = ''
    file_formatter = ''

    def __new__(classtype, *args, **kwargs):
        _logger_init_lock.acquire()
        if classtype != type(classtype.__instance):
            classtype.__instance = object.__new__(classtype, *args, **kwargs)
            classtype.__instance.init()

        _logger_init_lock.release()
        return classtype.__instance

    def init(self):
        # 创建日志目录
        global log_dir, log_name
        self.log_dir = log_dir
        self.log_name = log_name

        self.is_debug = True
        self.is_info = True
        self.is_warn = True
        self.is_error = True

        self.logger_formatter = "[%(asctime)-15s,%(levelname)s] %(message)s"
        self.file_formatter = "[%(asctime)-15s,%(levelname)s] %(message)s"
        self._init_logger()

        # self._init_sentry()

    def _init_logger(self):
        # 初始化logger
        logging.basicConfig(format=self.logger_formatter)
        self.logger = logging.getLogger("_sys")
        self.logger.setLevel(logging.DEBUG)

        # info、warn、error都放到info文件
        # error单独放到error文件
        for t in (("info", logging.INFO),
                  ("error", logging.ERROR)):
            filehandler = MulanTimedRotatingFileHandler(self.log_dir,
                                                        "%s.%s" % (self.log_name, t[0]))
            filehandler.suffix = "%Y%m%d.log"
            filehandler.setLevel(t[1])
            filehandler.setFormatter(logging.Formatter(self.file_formatter))
            self.logger.addHandler(filehandler)

        # debug 单独放到debug文件
        filehandler = MulanTimedRotatingFileHandler(self.log_dir,
                                                    "%s.debug" % self.log_name)
        filehandler.suffix = "%Y%m%d.log"
        filehandler.setLevel(logging.DEBUG)
        filehandler.setFormatter(logging.Formatter(self.file_formatter))
        self.logger.addHandler(filehandler)

    def _init_sentry(self):
        try:
            self.sentry = raven.Client(
                    dsn='',
                    # inform the client which parts of code are yours
                    # include_paths=['my.app']
                    # include_paths=[__name__.split('.', 1)[0]],

                    # pass along the version of your application
                    # release='1.0.0'
                    # release=raven.fetch_package_version('my-app')
                    # release=raven.fetch_git_sha(os.path.dirname(__file__)),
            )
        except:
            print 'sentry disable!'

    def get_logger(self):
        return self.logger

    def debug(self, msg, sentryable=False, tags={}, extra={}):
        if self.sentry and self.is_debug:
            self.logger.debug(msg)
            if sentryable:
                try:
                    self.sentry.captureMessage(msg, level='info', tags=tags, extra=extra)
                except:
                    self.init_sentry()

    def info(self, msg, sentryable=False, tags={}, extra={}):
        if self.is_info:
            self.logger.info(msg)
            if self.sentry and sentryable:
                try:
                    self.sentry.captureMessage(msg, level='info', tags=tags, extra=extra)
                except:
                    self.init_sentry()

    def warn(self, msg, sentryable=False, tags={}, extra={}):
        if self.is_warn:
            self.logger.warn(msg)
            if self.sentry and sentryable:
                try:
                    self.sentry.captureMessage(msg, level='warning', tags=tags, extra=extra)
                except:
                    self.init_sentry()

    def error(self, msg, sentryable=True, tags={}, extra={}):
        if self.is_error:
            self.logger.error(msg)
            if self.sentry and sentryable:
                try:
                    self.sentry.captureMessage(msg, level='error', tags=tags, extra=extra)
                except:
                    self.init_sentry()

    def exception(self, msg='', sentryable=True, tags={}, extra={}):
        self.logger.exception(msg)
        if self.sentry and sentryable:
            try:
                self.sentry.captureException(level='error', tags=tags, extra=extra)
            except:
                self.init_sentry()

logger = Logger()

if __name__ == "__main__":

    # logger.debug('debug')
    # logger.warn('tr-warn')
    # logger.info('ds-info')
    # logger.error('ss-error')

    logger.info('测试一下', sentryable=False, extra={'data': '口可口可'})
