import requests

import json

from Config import keys

class ConversionException(Exception):
    pass

class MoneyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amoute: str):
        if quote == base:
            raise ConversionException(f'Невозможно перевести одинаковые валюты "{base}".')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту "{quote}".')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту "{base}".')
        try:
            amoute = float(amoute)
        except ValueError:
            raise ConversionException(f'Не удалось обработать количество "{amoute}".')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        total_base = total_base * amoute
        return total_base