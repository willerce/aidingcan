#-*- coding:UTF-8-*-
from sqlalchemy.orm import relationship
from canku.extensions import db


class FoodCategory(db.Model):
    """食品分类模型"""

    __tablename__ = 'foodcategories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(32), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'))
    foods = relationship('Food', lazy='dynamic')

    def __init__(self, name, shop_id):
        self.name = name
        self.shop_id = shop_id

    def __repr__(self):
        return '<FoodCategory %r>' % self.name

    @staticmethod
    def findAllByShopId(shop_id):
        return FoodCategory.query.filter(FoodCategory.shop_id == shop_id).all()


class Food(db.Model):
    """食品模型"""

    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(32))
    price = db.Column(db.Float)
    week = db.Column(db.Integer, default=-1)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'))
    foodcategory_id = db.Column(db.Integer, db.ForeignKey('foodcategories.id'))

    def __init__(self, name, price, shop_id, week, food_category_id):
        self.name = name
        self.price = price
        self.shop_id = shop_id
        self.week = week
        self.food_category_id = food_category_id

    def __repr__(self):
        return '<Shop %r>' % self.name

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'week': self.week
        }


