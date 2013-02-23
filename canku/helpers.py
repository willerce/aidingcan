#-*- coding:UTF-8-*-
from flask import json


def get_week(num):
    week = {0: u'全部', 1: u'星期一', 2: u'星期二', 3: u'星期三', 4: u'星期四', 5: u'星期五', 6: u'星期六', 7: u'星期天'}
    return week[num]


def price_format(price):
    if price % 1 == 0:
        return int(price)
    return price


def json_load(text):
    return json.loads(text)