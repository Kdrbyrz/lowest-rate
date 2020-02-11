import os

from flask import Flask
from redis import Redis

app = Flask(__name__)

AVAILABLE_CURRENCY_UNITS = ['usd', 'gbp', 'eur']
host_name = os.getenv('host_name')

if not app.config.get('DEBUG'):
    redis = Redis(host='redis')
else:
    redis = Redis()

from app import routes
