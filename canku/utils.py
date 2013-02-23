#-*- coding:UTF-8-*-

from datetime import datetime
from flask.ext.login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pytz


def get_weekday():
    return get_now().weekday() + 1


def get_now():
    return datetime.now(pytz.timezone(pytz.country_timezones('cn')[0]))


def generate_password(password):
    return generate_password_hash(password)


def check_password(pwhash, password):
    if password is None:
        return False
    return check_password_hash(pwhash, password)


def get_current_user():
    return current_user


def get_currentt_user_id():
    return current_user.id


def get_currentt_user_group():
    if current_user.group:
        return current_user.group
    else:
        return None


def get_currentt_user_group_id():
    if current_user.group:
        return current_user.group_id
    else:
        return None


def logout():
    logout_user()


def login(user):
    login_user(user)
