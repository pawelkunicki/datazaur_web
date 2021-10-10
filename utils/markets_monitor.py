import os
from utils.compare_timestamps import *
import investpy
import pandas as pd
import datetime
from static.data.default_countries import DEFAULT_COUNTRIES
from static.data.default_indices import GENERAL_INDICES

def check_indices_files():
    return

def get_indices_table():
    INDICES_FILE = 'indices.csv'
    if INDICES_FILE in os.listdir() and compare_timestamps(300, INDICES_FILE):
        return pd.read_csv(INDICES_FILE, index_col=0)

    indices = GENERAL_INDICES
    result = pd.DataFrame(columns=['Country', 'Index', 'Price', '24h Δ'])
    print(result)
    for k, v in indices.items():
        print(k, v)
        for indx in v:
            try:
                data = investpy.get_index_recent_data(indx, k)['Close'].iloc[-2:]
                print(data)
                result.loc[len(result)] = {'Country': k, 'Index': indx, 'Price': data[1],
                                        '24h Δ': 100 * (data[1] - data[0]) / data[0]}

                print(result)
            except Exception as e:
                print(f'error {e}')

    print(result)
    result.iloc[:, 2:] = result.iloc[:, 2:].astype(float).round(2)
    result.to_csv('indices.csv')
    return result


def get_bonds_table(tenor='10Y'):
    result = []
    today = datetime.date.today()
    today_date = datetime.datetime.strptime(str(today), "%Y-%m-%d").strftime("%d/%m/%Y")

    n_days = find_last_day(today)
    prev_day = today - datetime.timedelta(days=n_days)
    prev_date = datetime.datetime.strptime(str(prev_day), "%Y-%m-%d").strftime("%d/%m/%Y")

    countries = investpy.get_bond_countries()

    for country in countries:
        bond = country + ' ' + tenor
        try:
            data = investpy.get_bond_historical_data(f'{bond}', from_date=prev_date, to_date=today_date).iloc[-2:]
            print(data)
            result += [bond, data.iloc[-1, 3], data.iloc[-1, 3] - data.iloc[-2, 3]]
            print(result)

        except Exception as e:
            print(f'error {e}')
    print(result)
    return result


def find_last_day(today):
    if today.isoweekday() == 7:
        return 2
    elif today.isoweekday() == 1:
        return 3
    else:
        return 1



def get_yield_curves():
    result = {}
    countries = DEFAULT_COUNTRIES
    for country in countries:
        try:
            data = investpy.get_bonds_overview(country)[['name', 'last', 'change']]
            data.columns = ['Bond', 'Yield', '24h Δ']
            result[country] = data.to_html()
            print(result)
        except Exception as e:
            print(f'error {e}')

    print(result)
    #pd.DataFrame(result).to_csv('yield_curves.csv')
    return result

