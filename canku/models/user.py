#-*- coding:UTF-8-*-
from flask.ext.sqlalchemy import BaseQuery
from werkzeug.security import check_password_hash
from canku.extensions import db


class UserQuery(BaseQuery):
    def authenticate(self, email, password):
        user = self.filter(User.email == email).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    def is_exists(self, email):
        return self.filter(User.email == email).first()


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    query_class = UserQuery

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.Unicode(50))
    name = db.Column(db.Unicode(50))
    figureurl = db.Column(db.Text)
    join = db.Column(db.DateTime)
    role = db.Column(db.Unicode(10))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    connects = db.relationship('Connect', backref='user', lazy="dynamic")

    def __init__(self, nickname=None, name=None, join=None, role=None, group_id=None, figureurl=None):
        self.nickname = nickname
        self.name = name
        self.join = join
        self.role = role
        self.group_id = group_id
        self.figureurl = figureurl

    def __repr__(self):
        return '<User %r>' % self.name

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Connect(db.Model):
    """第三方登录"""

    __tablename__ = 'connects'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    openid = db.Column(db.Integer)
    access_token = db.Column(db.Unicode(32))
    app = db.Column(db.Unicode(10))

    def __init__(self, openid, access_token, app):
        self.openid = openid
        self.access_token = access_token
        self.app = app

    def __repr__(self):
        return '<Connect %r>' % self.app

