import requests
import investpy
import os
from utils.compare_timestamps import *
import investpy
import pandas as pd
import datetime
from static.data.default_countries import DEFAULT_COUNTRIES
from static.data.default_indices import GENERAL_INDICES

from .formatting import *

CRYPTOCOMPARE_KEY = os.environ.get('CRYPTOCOMPARE_KEY')
FILES = {'crypto': 'crypto.csv', 'forex': 'forex.csv', 'indices': 'indices.csv', 'yields': 'yields.csv',
         'commodities': 'commodities.csv'}
REFRESH_RATE = 600
COLUMNS = ['Instrument', 'Price', '24h Δ']
RESULT_DF = pd.DataFrame(columns=COLUMNS)
CURRENCY = settings.DEFAULT_CURRENCY
TENOR = '10Y'


def all_markets_data(refresh_rate=REFRESH_RATE):
    data = {}
    coins_file = FILES['crypto']
    if compare_timestamps(refresh_rate, coins_file):
        data['crypto'] = pd.read_csv(coins_file, index_col=0).iloc[:20, :]
    else:
        data['crypto'] = coins_by_mcap().iloc[:20, :]
    print(f'1{data}')

    fx_file = FILES['forex']
    if compare_timestamps(refresh_rate, fx_file):
        data['forex'] = pd.read_csv(fx_file, index_col=0).iloc[0]
    else:
        data['forex'] = get_fx_rates(CURRENCY)

    print(f'2{data}')

    indices_file = FILES['indices']
    if compare_timestamps(refresh_rate, indices_file):
        data['indices'] = pd.read_csv(indices_file, index_col=0)
    else:
        data['indices'] = get_indices_table()

    print(f'3{data}')

    yields_file = FILES['yields']
    if compare_timestamps(refresh_rate, yields_file):
        data['yields'] = pd.read_csv(yields_file, index_col=0)
    else:
        data['yields'] = get_yields_table(TENOR)

    print(f'4{data}')
    commodities_file = FILES['commodities']
    if compare_timestamps(refresh_rate, commodities_file):
        data['commodities'] = pd.read_csv(commodities_file, index_col=0)
    else:
        data['commodities'] = get_commodities()

    print(f'5{data}')

    for k, v in data.items():

        v.to_csv(f'{k}.csv')
        data[k] = pd.DataFrame(v).to_html(escape=False)

    return data


def check_indices_files():
    return

def get_indices_table():
    indices = GENERAL_INDICES
    result = pd.DataFrame(columns=['Index', 'Price', '24h Δ'])
    for k, v in indices.items():
        for indx in v:
            try:
                data = investpy.get_index_recent_data(indx, k)['Close'].iloc[-2:]
                diff = (data[1] - data[0]).__round__(2)
                diff_pct = (100 * diff / data[0]).__round__(2)
                result.loc[len(result)] = {'Index': f"""{indx} ({k.title()})""",
                                           'Price': data[1],
                                           '24h Δ': f"{diff} ({diff_pct}%)"}
            except Exception as e:
                print(f'error {e}')

    result.iloc[:, 1] = result.iloc[:, 1].astype(float).round(2)
    result.iloc[:, 2] = result.iloc[:, 2].apply(color_cell)
    return result


def get_yields_table(tenor='10Y'):
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
            diff = (data['Close'].iloc[1] - data['Close'].iloc[0]).__round__(2)
            diff_pct = (100 * diff / data['Close'].iloc[0]).__round__(2)
            result.loc[len(result)] = [bond.title(), data['Close'].iloc[-1], f'{diff.__round__(2)} ({diff_pct.__round__(2)}%)']
        except Exception as e:
            print(f'error {e}')
    result['Yield'] = result['Yield'].astype('float64').round(3)
    result['24h Δ'] = result['24h Δ'].apply(color_cell)
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
    cols = ['name', 'country', 'last', 'change', 'change_percentage', 'currency']
    result_cols = ['Instrument', 'Price', '24h Δ']
    result = pd.DataFrame(columns=result_cols)

    for group in investpy.get_commodity_groups():
        table = investpy.get_commodities_overview(group)[cols]
        table['Instrument'] = f"{table['name']} ({table['country']})"
        table['Price'] = f"{table['last']} ({table['currency']})"
        table['24h Δ'] = f"{table['change']} ({table['change_percentage']})"
        result = result.append(table[result_cols], ignore_index=True)

    #result.iloc[:, 1] = result.iloc[:, 1].astype(float).round(2)
    result.iloc[:, 2] = result.iloc[:, 2].apply(color_cell)

    return result




def get_fx_rates(base_currency):
    return investpy.get_currency_crosses_overview(base_currency)[['symbol', 'bid', 'change', 'change_percentage']]



def get_coins_info():
    url = f'https://min-api.cryptocompare.com/data/all/coinlist?api_key={CRYPTOCOMPARE_KEY}'
    data = pd.DataFrame(requests.get(url).json()['Data']).transpose()[['Id', 'Name', 'Symbol', 'CoinName',
                                                                       'FullName', 'Description', 'Algorithm',
                                                                       'ProofType', 'TotalCoinsMined',
                                                                       'CirculatingSupply', 'MaxSupply',
                                                                       'BlockReward', 'AssetWebsiteUrl',
                                                                       'IsUsedInDefi', 'IsUsedInNft']]
    return data

def get_coins_data():
    coins_file = FILES['crypto']
    if coins_file not in os.listdir() or not compare_timestamps(300, coins_file):
        return coins_by_mcap()
    else:
        return pd.read_csv(coins_file, index_col=0)


def coins_by_mcap():
    coins_file = FILES['crypto']
    url = f'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=100&tsym={CURRENCY}&api_key={CRYPTOCOMPARE_KEY}'
    cols = f'CoinInfo.Name CoinInfo.FullName CoinInfo.Url RAW.{CURRENCY}.PRICE RAW.{CURRENCY}.CHANGE24HOUR ' \
           f'RAW.{CURRENCY}.CHANGEPCTHOUR RAW.{CURRENCY}.CHANGEPCT24HOUR ' \
           f'RAW.{CURRENCY}.TOTALVOLUME24HTO ' \
           f'RAW.{CURRENCY}.MKTCAP RAW.{CURRENCY}.SUPPLY RAW.{CURRENCY}.LASTUPDATE'.split()

    df = pd.json_normalize(requests.get(url).json()['Data']).loc[:, cols]
    print(df)  #
    #df.columns = ['Symbol', 'Name', 'Url', 'Price',  '1h Δ', '24h Δ', 'Volume', 'Mkt cap', 'Supply', 'Updated']
    print(df.columns)
    df = prepare_df_save(df)
    df.to_csv(coins_file)

    df = prepare_df_display(df, cols_to_split=[3, 4, 5, 6, 7, 8], upd_col=True, round_decimals=4)
    #df.iloc[:, 2:4] = df.iloc[:, 2:4].applymap(lambda x: round_number(x, 4))
    #df[['1h Δ', '24h Δ']] = df[['1h Δ', '24h Δ']].applymap(color_cell)
    return df













