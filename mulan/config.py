# -*- coding:utf-8 -*-
import os
import logging

project_name = "mulan-data-analysis"
basedir = os.path.abspath(os.path.dirname(__file__))

COMET_TIMEOUT = 60  # sec
COMET_POLL_TIME = 2

"""
    应用配置类
    ~~~~~~~~~~~~
"""


class Config(object):
    """
        基本配置类
    """
    DEBUG = False
    TESTING = False
    VERIFY_EMAIL = True
    VERIFY_USER = True

    ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))
    STATIC_FOLDER = os.path.join(ROOT_FOLDER, 'static', '')
    # 根目录的static文件，BEA要求static要在根目录
    # STATIC_FOLDER = os.path.join(os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir)), 'mulantrip', 'static/')

    #: site
    SITE_TITLE = '桂林电子科技大学新闻汇总系统'

    #: session
    SESSION_COOKIE_NAME = '_s'
    # SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30

    #: account
    SECRET_KEY = '87B34784v4FD057x5KQbzbSi48MiF'
    PASSWORD_SECRET = 'kf'

    #: email settings
    MAIL_SERVER = 'smtp.126.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_PORT = 587
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = ''  # ('name', 'noreply@email.com')

    # MAIL_SERVER = 'smtp.qq.com'
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL= False
    # MAIL_PORT=587
    # MAIL_USERNAME = 'noreply@mulantech.com'
    # MAIL_PASSWORD = 'passowrd'
    # MAIL_DEFAULT_SENDER = 'noreply@mulantech.com'

    # leancloud
    APP_ID = "Xmh3GP4wHdgz4jPVpaW6jQYM-gzGzoHsz"
    MASTER_KEY = "j8VdYDUkWaKGTirQQrKsFeUC"


class Dev(Config):
    """
        开发环境配置类
    """
    DEBUG = True

    #: sqlalchemy
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(os.getcwd(), 'db.sqlite')
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % ('','','host',4050,'')
    # SQLALCHEMY_POOL_SIZE = 100
    # SQLALCHEMY_POOL_TIMEOUT = 10
    # SQLALCHEMY_POOL_RECYCEL = 3600


class Testing(Config):
    """
    测试环境配置类
    """
    TESTING = True
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False

    # leancloud
    APP_ID = "tQVcROVTI43C5NTD5TiNKG0r-gzGzoHsz"
    MASTER_KEY = "vbiLt5t7YgzIPPREKK1Fj2la"
    #: sqlalchemy
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(os.getcwd(), 'db.sqlite')


class Release(Config):
    """
    发布环境
    """
    DEBUG = False

    SITE_URL = 'http://127.0.0.1'
    #: sqlalchemy
    # sqlite
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(
    #         os.getcwd(), 'db.sqlite'
    # )
    # mysql
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % ('db-username','db-password','db-url','db-name')
    # SQLALCHEMY_POOL_SIZE = 100
    # SQLALCHEMY_POOL_TIMEOUT = 10
    # SQLALCHEMY_POOL_RECYCEL = 3600

