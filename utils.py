import requests
import json


def get_currencies_hh(valute: str) -> float:
    """
    Функция возвращает курс валюты к рублю для HeadHunter
    :param valute:
    :return:
    """
    rate = 0
    url = f"https://api.hh.ru/dictionaries"
    response = requests.get(url)
    response_data = json.loads(response.text)
    for valut in response_data["currency"]:
        if valute == valut["code"]:
            rate = float(valut["rate"])
    return rate
