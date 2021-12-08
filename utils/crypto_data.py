import pandas as pd
import numpy as np
import requests
import os
import json
from django.conf import settings
from utils.decorators import prep_crypto_display, load_or_save
from .formatting import prepare_df_display

coins_file = settings.CRYPTO_FILE
currency = settings.DEFAULT_CURRENCY
api_key = os.environ.get('CRYPTOCOMPARE_KEY')
base_cryptocompare_url = settings.BASE_CRYPTOCOMPARE_URL


def watchlist_prices(watchlist):
    pass

def get_coins_info():
    url = f'https://min-api.cryptocompare.com/data/all/coinlist?api_key={api_key}'
    data = pd.DataFrame(requests.get(url).json()['Data']).transpose()[['Id', 'Name', 'Symbol', 'CoinName',
                                                                       'FullName', 'Description', 'Algorithm',
                                                                       'ProofType', 'TotalCoinsMined',
                                                                       'CirculatingSupply', 'MaxSupply',
                                                                       'BlockReward', 'AssetWebsiteUrl',
                                                                       'IsUsedInDefi', 'IsUsedInNft']]
    return data

def update_coin_prices():
    url = f'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=100&tsym={currency}&api_key={api_key}'
    cols = f'CoinInfo.Name CoinInfo.FullName CoinInfo.Url RAW.{currency}.PRICE '


@load_or_save('crypto.csv', 1200)
def top_coins_by_mcap():
    url = f'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=100&tsym={currency}&api_key={api_key}'
    cols = f'CoinInfo.Name CoinInfo.FullName CoinInfo.Url RAW.{currency}.PRICE ' \
           f'RAW.{currency}.CHANGEPCTHOUR RAW.{currency}.CHANGEPCT24HOUR ' \
           f'RAW.{currency}.TOTALVOLUME24HTO ' \
           f'RAW.{currency}.MKTCAP RAW.{currency}.SUPPLY RAW.{currency}.LASTUPDATE'.split()
    df = pd.json_normalize(requests.get(url).json()['Data']).loc[:, cols]
    df.columns = ['Symbol', 'Name', 'Url', 'Price', '1h Δ', '24h Δ', '24h vol', f'Market cap ({currency})',
                  'Supply', 'Updated']
    df.dropna(inplace=True)
    df.iloc[:, 3:6] = df.iloc[:, 3:6].astype('float64').round(3)
    df.iloc[:, 6:9] = df.iloc[:, 6:9].astype('int64')

    return prepare_df_display(df)



@load_or_save('exchanges.csv', 86400)
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



