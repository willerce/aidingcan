# -*- coding: utf-8 -*-

from canku.helpers import get_week, price_format
from tests import TestCase


class TestPriceFormat(TestCase):

    def test_integer(self):
        assert price_format(20) == 20

    def test_decimal1(self):
        assert price_format(20.0) == 20

    def test_decimal2(self):
        assert price_format(20.1) == 20.1


class TestGetWeek(TestCase):

    def test_all(self):
        assert get_week(0) == u'全部'

    def test_mon(self):
        assert get_week(1) == u'星期一'

    def test_tue(self):
        assert get_week(2) == u'星期二'

    def test_wed(self):
        assert get_week(3) == u'星期三'

    def test_thu(self):
        assert get_week(4) == u'星期四'

    def test_fri(self):
        assert get_week(5) == u'星期五'

    def test_sat(self):
        assert get_week(6) == u'星期六'

    def test_sun(self):
        assert get_week(7) == u'星期天'