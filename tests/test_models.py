#-*- coding:UTF-8-*-
from flask.ext.testing import TestCase
from canku.extensions import db
from canku.models import City


class TestCity(TestCase):

    def test_empty_city(self):
        cities = City.query.all()
        assert cities == []

    def test_city(self):
        city = City(u'福州')

        db.session.add(city)
        db.session.commit()

        assert City.query.count() == 1