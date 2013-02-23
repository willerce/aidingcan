#-*- coding:UTF-8-*-

from flask.ext.sqlalchemy import SQLAlchemy
from canku.libs.connect_qq import QQAPIClient
from canku.libs.connect_sina import SinaAPIClient


__all__ = ['db']

db = SQLAlchemy()
