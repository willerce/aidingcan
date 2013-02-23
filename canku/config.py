#-*- coding:utf-8 -*-
from flask import json
import os

__author__ = 'willerce'


class DefaultConfig(object):
    DEBUG = True
    SECRET_KEY = "SECRET_KEY"
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/canku?charset=utf8'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_CONVERT_UNICODE = False

    SINA_APP_KEY = '3104287767'
    SINA_APP_SECRET = 'd22d42c3ec17bb43bb50d7f817e5a160'
    SINA_CALLBACK_URL = 'http://xx.aidingcan.com/connect/sina/authorized'

    QQ_APP_KEY = '100247774'
    QQ_APP_SECRET = '532c151ddafc5ade894109a83d4bf5bf'
    QQ_CALLBACK_URL = 'http://xx.aidingcan.com/connect/qq/authorized'


class TestConfig(object):
    DEBUG = True
    SECRET_KEY = "SECRET_KEY"
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/canku?charset=utf8'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_CONVERT_UNICODE = False

    SINA_APP_KEY = '3104287767'
    SINA_APP_SECRET = 'd22d42c3ec17bb43bb50d7f817e5a160'
    SINA_CALLBACK_URL = 'http://xx.aidingcan.com/connect/sina/authorized'

    QQ_APP_KEY = '100247774'
    QQ_APP_SECRET = '532c151ddafc5ade894109a83d4bf5bf'
    QQ_CALLBACK_URL = 'http://xx.aidingcan.com/connect/qq/authorized'

class ProductionConfig(object):
    DEBUG = False
    SECRET_KEY = "cankuadc_sk"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_CONVERT_UNICODE = False
    SQLALCHEMY_DATABASE_URI = "mysql://root:tb592rootadcmysql@localhost/canku?charset=utf8"

    SINA_APP_KEY = '3104287767'
    SINA_APP_SECRET = 'd22d42c3ec17bb43bb50d7f817e5a160'
    SINA_CALLBACK_URL = 'http://www.aidingcan.com/connect/sina/authorized'

    QQ_APP_KEY = '100247774'
    QQ_APP_SECRET = '532c151ddafc5ade894109a83d4bf5bf'
    QQ_CALLBACK_URL = 'http://www.aidingcan.com/connect/qq/authorized'