import json
import os

from app import AVAILABLE_CURRENCY_UNITS, app
from app import redis
from app.functions import is_cache_available_for_ten_mins, parse_rate, compare_providers, compare_daily_rate, \
    fill_values
from app.models import Provider


@app.route('/rate/<string:currency>/', methods=['GET'])
def lowest_rate(currency):
    currency = currency.lower()
    if currency not in AVAILABLE_CURRENCY_UNITS:
        return 'Lutfen gecerli bir para birimi giriniz'
    rate = is_cache_available_for_ten_mins()
    if rate:
        rate = parse_rate(rate)
        return json.dumps(rate['rates'][currency])
    providers_env = json.loads(os.getenv('providers'))
    provider_list = []
    for provider in providers_env:
        provider_list.append(Provider(provider['url'], provider['code_key'], provider['rate_key']))
    rate = compare_providers(provider_list)
    return json.dumps(rate[currency])


@app.route('/daily/rate/<string:currency>/', methods=['GET'])
def daily_rate(currency):
    currency = currency.lower()
    if currency not in AVAILABLE_CURRENCY_UNITS:
        return 'Lutfen gecerli bir para birimi giriniz'

    redis_keys_for_daily = redis.keys(pattern='daily_*')
    daily_values = fill_values(redis_keys_for_daily)
    lowest_daily_rate = compare_daily_rate(daily_values)
    if len(lowest_daily_rate):
        return json.dumps(lowest_daily_rate[currency])
    return 'Gunluk veri bulunamadi'
