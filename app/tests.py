import json
import unittest

import app
from app import redis
from app.models import Provider
from app.functions import compare_providers, compare_daily_rate, is_cache_available_for_ten_mins, fill_values
from app.routes import lowest_rate, daily_rate


class TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.redis = redis

        self.test_provider1 = Provider('http://www.mocky.io/v2/5d19ec932f00004e00fd7326', 'code', 'rate')
        self.test_provider1.rate_data = {
            'usd': 6, 'eur': 5, 'gbp': 1
        }
        self.test_provider2 = Provider('http://www.mocky.io/v2/5d19ec932f00004e00fd7326', 'code', 'rate')
        self.test_provider2.rate_data = {
            'usd': 2, 'eur': 1, 'gbp': 2
        }
        self.daily_test_data = [{'usd': 1, 'eur': 2, 'gbp': 3}, {'usd': 2, 'eur': 2, 'gbp': 7},
                                {'usd': 3, 'eur': 2, 'gbp': 5}]

    def tearDown(self) -> None:

        self.redis.flushall()


    def test_compare_providers(self):
        providers = [self.test_provider1, self.test_provider2]
        lowest_rates = compare_providers(providers)
        self.assertEqual(lowest_rates, {'usd': 2, 'eur': 1, 'gbp': 1})

    def test_compare_daily_rate(self):
        lowest_daily_rates = compare_daily_rate(self.daily_test_data)
        self.assertEqual(lowest_daily_rates, {'usd': 1, 'eur': 2, 'gbp':3})

    def test_is_cache_available_for_ten_mins(self):
        is_cached = is_cache_available_for_ten_mins()
        self.assertFalse(is_cached)

        self.redis.hmset('rate_ten_mins', {'mock': 'mock'})
        is_cached = is_cache_available_for_ten_mins()

        self.assertTrue(is_cached)

    def test_fill_values(self):
        expected_filled_keys = [{"usd": "1", "eur": "2", "gbp": "3"}, {"usd": "3", "eur": "4", "gbp": "5"}]
        keys = [b'key1', b'key2']
        self.redis.hmset("key1", {"rates": json.dumps({"usd": "1", "eur": "2", "gbp": "3"})})
        self.redis.hmset("key2", {"rates": json.dumps({"usd": "3", "eur": "4", "gbp": "5"})})
        filled_keys = fill_values(keys)
        self.assertEqual(filled_keys, expected_filled_keys)

    def test_rate_usd_use_cache(self):
        self.redis.hmset("rate_ten_mins", {"rates": json.dumps({"usd": 1, "eur": 2, "gbp": 3}), 'providers': json.dumps({"test": "test"}), 'time_stamp': 1.1})
        resp = lowest_rate('usd')
        self.assertEqual("1", resp)

    def test_daily_usd_rate_cache(self):
        self.redis.hmset("daily_1", {"rates": json.dumps({"usd": 1, "eur": 2, "gbp": 3})})
        resp = daily_rate('usd')
        self.assertEqual("1", resp)


