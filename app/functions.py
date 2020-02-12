import datetime
import json

from app import redis


def compare_providers(providers):
    lowest_rates = {}
    currency_units = providers[0].rate_data.keys()
    for currency_unit in currency_units:
        currency_values = list(map((lambda x: x.rate_data.get(currency_unit)), providers))
        lowest_rates[currency_unit] = min(currency_values)

    make_cache_rate(lowest_rates, providers)
    return lowest_rates


def compare_daily_rate(daily_data: list):
    if not len(daily_data):
        return []
    lowest_rates = {}
    currency_units = daily_data[0].keys()
    for currency_unit in currency_units:
        currency_values = list(map((lambda x: x.get(currency_unit)), daily_data))
        lowest_rates[currency_unit] = min(currency_values)

    return lowest_rates


def is_cache_available_for_ten_mins():
    rate_ten_mins = redis.hgetall('rate_ten_mins')
    if rate_ten_mins:
        return rate_ten_mins
    return False


def make_cache_rate(rates, providers):
    ts_now = datetime.datetime.now().timestamp()

    payload = {
        'time_stamp': str(ts_now),
        'rates': json.dumps(rates),
        'providers': json.dumps([provider.url for provider in providers])}
    redis.hmset('rate_ten_mins', payload)
    redis.expire('rate_ten_mins', 10 * 60)
    redis.hmset('daily_ ' + str(ts_now), payload)
    redis.expire('daily_ ' + str(ts_now), 60 * 60 * 24)


def fill_values(keys: list):
    filled_keys = []
    for key in keys:
        filled_value = redis.hmget(key, 'rates')[0]
        filled_keys.append(json.loads(filled_value.decode('utf-8')))
    return filled_keys


def parse_rate(rate):
    rate['rates'] = json.loads(rate[b'rates'].decode('utf-8'))
    rate['providers'] = json.loads(rate[b'providers'].decode('utf-8'))
    rate['time_stamp'] = float(rate[b'time_stamp'].decode('utf-8'))
    return rate
