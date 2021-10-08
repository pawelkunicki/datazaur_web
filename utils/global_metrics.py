import pandas as pd
from django.conf import settings

filename = '~/PycharmProjects/datazaur_web/crypto.csv'
currency = 'USD'

def market_dominance(top_n_coins):
    coins = pd.read_csv(filename, index_col=0).loc[:top_n_coins, f'Market cap ({currency})']
    print(coins)



print(market_dominance(10))