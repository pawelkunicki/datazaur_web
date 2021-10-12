'''
from forex_python.converter import CurrencyRates
import pandas as pd
import os
import investpy
from django.conf import settings
from .compare_timestamps import compare_dates

CURRENCY = settings.DEFAULT_CURRENCY
SORTED_CURRENCIES = settings.SORTED_CURRENCIES
FILE = 'forex.csv'


def get_rates(currency=CURRENCY):
    rates = CurrencyRates()
    if FILE not in os.listdir():
        fx_rates = pd.Series(rates.get_rates(currency))
    else:
        fx_rates = pd.read_csv(FILE, index_col=0).iloc[0, :]
        if fx_rates.index[0] == currency:
            return fx_rates
        else:
            return pd.Series(rates.get_rates(currency)).astype(float).round(4)


def get_forex_matrix(currency=CURRENCY):
    if FILE in os.listdir() and compare_dates(FILE):
        return pd.read_csv(FILE, index_col=0)
    else:
        rates = pd.Series({currency: 1}).append(get_rates(currency))
        SORTED_CURRENCIES.remove(currency)
        SORTED_CURRENCIES.insert(0, currency)
        matrix = pd.DataFrame(index=SORTED_CURRENCIES, columns=SORTED_CURRENCIES)
        matrix.loc[currency, :] = rates
        matrix.loc[:, currency] = rates
        matrix = calculate_cross_rates(matrix, currency).astype(float).round(4)
        matrix.to_csv(FILE)
        print(matrix)
        return matrix


def calculate_cross_rates(matrix, base_currency):
    return matrix.apply(lambda x: matrix.loc[base_currency] / x.loc[base_currency]).transpose()



def get_fx_rates(base_currency):
    return investpy.get_currency_crosses_overview(base_currency)[['symbol', 'bid', 'change', 'change_percentage']]
'''



