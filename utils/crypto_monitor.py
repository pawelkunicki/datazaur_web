import pandas as pd
import numpy as np
import os
import requests
import json
from django.conf import settings
from utils.compare_timestamps import *


coins_file = settings.CRYPTO_FILE
currency = settings.DEFAULT_CURRENCY
api_key = settings.CRYPTOCOMPARE_API_KEY
base_cryptocompare_url = settings.BASE_CRYPTOCOMPARE_URL


def get_coins_info():
    url = f'https://min-api.cryptocompare.com/data/all/coinlist?api_key={api_key}'
    data = pd.DataFrame(requests.get(url).json()['Data']).transpose()[['Id', 'Name', 'Symbol', 'CoinName',
                                                                       'FullName', 'Description', 'Algorithm',
                                                                       'ProofType', 'TotalCoinsMined',
                                                                       'CirculatingSupply', 'MaxSupply',
                                                                       'BlockReward', 'AssetWebsiteUrl',
                                                                       'IsUsedInDefi', 'IsUsedInNft']]
    return data

def get_coins_data():
    if coins_file not in os.listdir() or not compare_timestamps(300, coins_file):
        return coins_by_mcap()
    else:
        return pd.read_csv(coins_file, index_col=0)


def coins_by_mcap():
    url = f'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=100&tsym={currency}&api_key={api_key}'
    cols = f'CoinInfo.Name CoinInfo.FullName CoinInfo.Url RAW.{currency}.PRICE ' \
           f'RAW.{currency}.CHANGEPCTHOUR RAW.{currency}.CHANGEPCT24HOUR ' \
           f'RAW.{currency}.TOTALVOLUME24HTO ' \
           f'RAW.{currency}.MKTCAP RAW.{currency}.SUPPLY RAW.{currency}.LASTUPDATE'.split()
    df = pd.json_normalize(requests.get(url).json()['Data']).loc[:, cols]
    df = prepare_df_save(df)
    df.to_csv(coins_file)
    df = prepare_df_display(df, cols_to_split=[2, 5, 6, 7], upd_col=True, round_decimals=6)
    return df



def add_hyperlinks(df):
    for col in ['Symbol', 'Name']:
        df[col] = df.apply(lambda x: f"""<a href={base_cryptocompare_url + x['Url']}>{x[col]}</a>""", axis=1)
    return df


def color_prices(x):
    if type(x) == str:
        x = float(x.replace('%', '').replace(',', '.'))
    return f"""<p class=green>{x}%</p>""" if x >= 0 else f"""<p class=red>{x}%</p>"""


def prepare_df_display(df, cols_to_split, upd_col, round_decimals):
    df = add_hyperlinks(df)
    if 'Url' in df.columns:
        df.drop('Url', inplace=True, axis=1)
    df[['1h Δ', '24h Δ']] = df[['1h Δ', '24h Δ']].round(2)
    df.iloc[:, 3:5] = df.iloc[:, 3:5].applymap(color_prices)
    df.loc[:, ['Price']] = df.loc[:, ['Price']].astype('float64')
    df.loc[:, ['Price']] = df.loc[:, ['Price']].round(round_decimals)
    df.iloc[:, cols_to_split] = df.iloc[:, cols_to_split].applymap(lambda x: format(x, ','))
    if upd_col:
        df['Updated'] = df['Updated'].apply(lambda x: pd.to_datetime(x * 10 ** 9))
    return df


def prepare_df_save(df):
    df.columns = ['Symbol', 'Name', 'Url', 'Price', '1h Δ', '24h Δ', '24h vol', f'Market cap ({currency})',
                  'Supply', 'Updated']
    df.dropna(inplace=True)
    df.iloc[:, 6:9] = df.iloc[:, 6:9].astype('int64')
    return df

def exchanges_by_vol():
    url = f'https://min-api.cryptocompare.com/data/exchanges/general?api_key={api_key}&tsym={currency}'
    df = pd.DataFrame(requests.get(url).json()['Data']).transpose()[
        ['Name', 'Country', 'Grade', 'TOTALVOLUME24H', 'AffiliateURL']]
    df['Name'] = df.apply(lambda x: f"""<a href={x['AffiliateURL']}>{x['Name']}</a>""", axis=1)
    df['24h vol (BTC)'] = df['TOTALVOLUME24H'].apply(lambda x: x['BTC'], True).round(3)
    df[f'24h vol ({currency})'] = df['TOTALVOLUME24H'].apply(lambda x: '%.3f' % x[currency], True)
    df = df.drop(['TOTALVOLUME24H', 'AffiliateURL'], axis=1).sort_values(by='24h vol (BTC)',
                                                                         ascending=False).reset_index(drop=True)
    vol_col = f'Volume ({currency})'
    df.columns = ['Name', 'Country', 'Grade', vol_col, 'Url']
    df.drop('Url', axis=1, inplace=True)
    df[vol_col] = list(map(lambda x: format(x, ','), df[vol_col]))
    return df

def global_metrics():
    return 1



