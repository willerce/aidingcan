#-*- coding:UTF-8-*-
from canku.extensions import db


class City(db.Model):
    """城市"""

    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(32))
    shops = db.relationship('Shop', backref=db.backref('city', lazy='joined'), lazy='dynamic')
    groups = db.relationship('Group', backref=db.backref('city', lazy='joined'), lazy='dynamic')

    def __init__(self, name):
        self.name = name