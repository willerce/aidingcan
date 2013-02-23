#-*- coding:UTF-8-*-
from flask.ext.login import LoginManager
import os

from flask import Flask

from canku import views, helpers, utils
from canku.models import User, Connect, Food, FoodCategory, Group, Order, Shop
from canku.config import DefaultConfig
from canku.extensions import db


DEFAULT_APP_NAME = "canku"
DEFAULT_BLUEPRINTS = (
    (views.frontend_bp, ""),
    (views.shop_bp, "/shop"),
    (views.group_bp, "/group")
    )


def create_app(config=None, app_name=None):
    if app_name is None:
        app_name = DEFAULT_APP_NAME

    app = Flask(app_name)

    app.template_folder = os.path.join(os.path.dirname(__file__), '_templates')
    app.static_folder = os.path.join(os.path.dirname(__file__), "_static")

    configure_app(app, config)
    configure_extensions(app)
    configure_template_filters(app)
    configure_blue_print(app, DEFAULT_BLUEPRINTS)

    return app


def configure_app(app=None, config=None):
    app.config.from_object(DefaultConfig())

    if config is not None:
        app.config.from_object(config)

    app.config.from_envvar('APP_CONFIG', silent=True)


def configure_extensions(app):
    db.app = app
    db.init_app(app)

    configure_login_manager(app)


def configure_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(userid):
        return User.query.get(userid)

    login_manager.login_view = "frontend.signin"


def configure_template_filters(app):
    @app.context_processor
    def utility_processor():
        return dict(get_week=helpers.get_week, json_load=helpers.json_load, price_format=helpers.price_format)


def configure_blue_print(app, blueprints):
    for blueprint, url_prefix in blueprints:
        if url_prefix:
            app.register_blueprint(blueprint, url_prefix=url_prefix)
        else:
            app.register_blueprint(blueprint)

