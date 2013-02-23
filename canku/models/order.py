#-*- coding:UTF-8-*-
from canku.extensions import db


class Order(db.Model):
    """订单模型"""

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    total = db.Column(db.Float)
    time = db.Column(db.DateTime)
    text = db.Column(db.Text)
    luck = db.Column(db.Integer)

    shop = db.relationship('Shop')
    user = db.relationship('User')

    def __init__(self, user_id, shop_id, group_id, total, time, text, luck):
        self.user_id = user_id
        self.shop_id = shop_id
        self.group_id = group_id
        self.total = total
        self.time = time
        self.text = text
        self.luck = luck

    def __repr__(self):
        return '<Order %r>' % (self.id)

