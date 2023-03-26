import requests
import json
from config import keys


class APIException(Exception):
    pass


class Currency:
    @staticmethod
    def get_price(quote, base, amount:float):
        try:
            quote_key=keys[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        try:
            base_key=keys[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        if quote_key == base_key:
            raise APIException(f'Невозможно перевести одинаковые валюты: {quote}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        url = f"https://api.exchangerate.host/convert?from={quote_key}&to={base_key}"
        r = requests.get(url)
        rate = json.loads(r.content)['info']['rate']
        return f"Цена {amount} {quote}: {round(rate*float(amount), 2)} {base}"
