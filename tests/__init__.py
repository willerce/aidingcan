#-*- coding:UTF-8-*-

from flask.ext.testing import TestCase as Base, Twill

from canku import create_app
from canku.config import TestConfig
from canku.extensions import db


class TestCase(Base):
    """
    Base TestClass for your application.
    """

    def create_app(self):
        app = create_app(TestConfig())
        self.twill = Twill(app, port=3000)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def assert_401(self, response):
        assert response.status_code == 401

    def login(self, **kwargs):
        response = self.client.post("/signin/", data=kwargs)
        assert response.status_code in (301, 302)

    def logout(self):
        response = self.client.get("/signout/")