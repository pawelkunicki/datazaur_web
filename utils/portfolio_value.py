import os

import pandas as pd
from forex_python.converter import CurrencyRates
from crypto.crypto_monitor import *
from utils.compare_timestamps import compare_timestamps
from django.conf import settings




def get_currency_value(base, quote, amount):
    rates = CurrencyRates()
    rate = rates.get_rate(base, quote)
    return amount * rate


def get_crypto_value(coin, quote, amount):
    coins_file = settings.CRYPTO_FILE
    currency = settings.DEFAULT_CURRENCY
    refresh_rate = settings.REFRESH_RATE
    if coins_file not in os.listdir() or not compare_timestamps(refresh_rate, coins_file):
        monitor = CryptoMonitor()
        c = monitor.coins_by_mcap()
    coins = pd.read_csv(coins_file, index_col=0)

    if currency != quote:
        rates = CurrencyRates()
        exchange_rate = rates.get_rate(currency, quote)
    else:
        exchange_rate = 1

    price = coins[coins['Symbol'] == coin]['Price'].iloc[0]
    return amount * price * exchange_rate


def get_portfolio_value(portfolio, currency):
    value = 0
    currencies = settings.SORTED_CURRENCIES
    for k, v in portfolio.items():
        if k in currencies:
            value += get_currency_value(k, currency, v)
        else:
            value += get_crypto_value(k, currency, v)

    return value
