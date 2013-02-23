#-*- coding:UTF-8-*-
from sqlalchemy import Column, Integer, Unicode, Text, Float, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from canku.extensions import db


class Shop(db.Model):
    """店铺模型"""

    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(32), nullable=False)
    address = Column(Unicode(120))
    tel = Column(Unicode(120))
    css = Column(Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    food_categories = db.relationship('FoodCategory', lazy="dynamic")
    foods = db.relationship('Food', lazy="dynamic")
    creator = db.relationship('User')

    def __init__(self, name, address, tel, city_id, creator_id, css=None):
        self.name = name
        self.address = address
        self.tel = tel
        self.city_id = city_id
        self.css = css
        self.creator_id = creator_id

    def __repr__(self):
        return '<Shop %r>' % self.name

    @staticmethod
    def get(id):
        return Shop.query.filter(Shop.id == id).first()

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'tel': self.tel
        }
