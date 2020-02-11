import requests


class Provider:
    rate_data = {}

    def __init__(self, url: str, code_key: str, rate_key: str):
        self.url = url
        self.code_key = code_key
        self.rate_key = rate_key
        self.get_rate()

    def get_rate(self):
        response = requests.get(self.url).json()

        for data in response:
            self.rate_data[data[self.code_key.lower()]] = float(data[self.rate_key])
