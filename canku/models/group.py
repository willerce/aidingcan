#-*- coding:UTF-8-*-
from canku import utils
from canku.extensions import db


group_shops = db.Table(
    'group_shops',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('shop_id', db.Integer, db.ForeignKey('shops.id'))
)


class Group(db.Model):
    """小组模型"""

    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(32))
    descrip = db.Column(db.Text)
    address = db.Column(db.Unicode(64))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    user_num = db.Column(db.Integer)
    created = db.Column(db.DateTime)
    creator_id = db.Column(db.Integer)
    users = db.relationship('User', backref=db.backref('group', lazy='joined'), lazy='dynamic')
    shops = db.relationship('Shop', secondary=group_shops, backref=db.backref('groups', lazy='dynamic'), lazy='dynamic')

    def __init__(self, name, descrip, address, city_id, creator_id, user_num=1, created=utils.get_now()):
        self.name = name
        self.descrip = descrip
        self.address = address
        self.city_id = city_id
        self.creator_id = creator_id
        self.user_num = user_num
        self.created = created