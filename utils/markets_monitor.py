import os
from utils.compare_timestamps import *
import investpy
import pandas as pd
import datetime
from static.data.default_countries import DEFAULT_COUNTRIES
from static.data.default_indices import GENERAL_INDICES
from .crypto_monitor import color_prices

def check_indices_files():
    return

def get_indices_table():
    INDICES_FILE = 'indices.csv'
    if INDICES_FILE in os.listdir():
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
    result.to_csv(INDICES_FILE)
    return result


def get_bonds_table(tenor='10Y'):
    YIELDS_FILE = 'yields.csv'
    if YIELDS_FILE in os.listdir():
        return pd.read_csv(YIELDS_FILE)

    result = pd.DataFrame(columns=['Bond', 'Yield', '24h Δ'])
    today = datetime.date.today()

    n_days_diff = find_days_diff(today)
    start_date = today - datetime.timedelta(days=n_days_diff)
    end_date = today - datetime.timedelta(days=n_days_diff-1)
    start_date = datetime.datetime.strptime(str(start_date), "%Y-%m-%d").strftime("%d/%m/%Y")
    end_date = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").strftime("%d/%m/%Y")

    countries = investpy.get_bond_countries()

    for country in countries:
        bond = country + ' ' + tenor
        try:
            data = investpy.get_bond_historical_data(f'{bond}', from_date=start_date, to_date=end_date).iloc[-2:]
            print(data)
            result.loc[len(result)] = [bond, data.iloc[-1, 3], data.iloc[-1, 3] - data.iloc[-2, 3]]
            print(result)

        except Exception as e:
            print(f'error {e}')
    print(result)
    result['Yield'] = result['Yield'].astype(float).round(3)
    result['24h Δ'] = result['24h Δ'].astype(float).round(4)
    result.to_csv(YIELDS_FILE)
    return result


def find_days_diff(today):
    if today.isoweekday() == 6:
        return 2
    elif today.isoweekday() == 7:
        return 3
    elif today.isoweekday() == 1:
        return 4
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



def get_commodities():
    cols = ['name', 'last', 'change_percentage', 'currency']
    COMMODITTIES_FILE = 'commodities.csv'
    if COMMODITTIES_FILE is os.listdir():
        return pd.read_csv(COMMODITTIES_FILE, index_col=0)

    result = pd.DataFrame(columns=cols)
    for group in investpy.get_commodity_groups():
        table = investpy.get_commodities_overview(group)[cols]
        result = result.append(table, ignore_index=True)

    result.iloc[:, 1:3] = result.iloc[:, 1:3].astype(float).round(2)
    result.iloc[:, 2] = result.iloc[:, 2].apply(color_prices)
    result.columns = ['Name', 'Price', '24h Δ', 'Currency']
    result.to_csv(COMMODITTIES_FILE)
    return result


