from django.contrib.auth.models import User
from watchlist.models import Watchlist

from markets.models import Currency
from crypto.models import Cryptocurrency, Exchange
from backup.crypto_monitor import *
from django.conf import settings

FX_FILE = 'static/data/iso-4217-currency-codes.csv'

def setup_fx_db():
    currency = settings.DEFAULT_CURRENCY
    currencies = settings.SORTED_CURRENCIES
    codes = pd.read_csv(FX_FILE)
    codes.drop_duplicates(subset=['Alphabetic_Code'], inplace=True, keep='first')
    codes.set_index('Alphabetic_Code', inplace=True)
    for curr in currencies:
        currency = Currency.objects.create(symbol=curr, name=codes.loc[curr, 'Currency'], country=codes.loc[curr, 'Entity'])
        currency.save()





def setup_crypto_db():
    coins = get_coins_info()
    coins.to_csv('coins_info.csv')
    coins.dropna(inplace=True)
    #coins = coins.applymap(lambda x: None if not x or x=='NaN' or x=='nan' else x)
    print(coins)
    for k, v in coins.iterrows():
        print(v)
        new_coin = Cryptocurrency.objects.create(symbol=v['Symbol'], name=v['CoinName'], description=v['Description'],
                                                 url=v['AssetWebsiteUrl'],  algorithm=v['Algorithm'],
                                                 proof_type=v['ProofType'], total_coins_mined=v['TotalCoinsMined'],
                                                 circulating_supply=v['CirculatingSupply'], max_supply=v['MaxSupply'],
                                                 used_in_defi=v['IsUsedInDefi'], used_in_nft=v['IsUsedInNft'],
                                                 block_reward=v['BlockReward'])
        new_coin.save()
    print('finito setup crypto')


def setup_exchanges_db():
    exchanges_file = settings.EXCHANGES_FILE
    if exchanges_file in os.listdir():
        exchanges = pd.read_csv(settings.EXCHANGES_FILE, index_col=1)
    else:
        exchanges = exchanges_by_vol()
        exchanges.to_csv(exchanges_file)
    for i, row in exchanges.iterrows():
        new_exchange = Exchange.objects.create(name=i, url=row['Url'], country=row['Country'],
                                               grade=row['Grade'])
        new_exchange.save()




# checks if database has as many objects as specified in settings (currencies are settings.SORTED_CURRENCIES,
# cryptos are 'Symbol' column of saved 'cryptos.csv' file
# True means that database has as many or more objects as specified in settings, hence no action is required
# False means that database doesn't have enough objects (according to settings) and objects should be created in DB
def check_db(db_object, settings_object):
    return db_object.objects.all().count() >= len(settings_object)


def setup_db():
    currencies = settings.SORTED_CURRENCIES
    exchanges_file = settings.EXCHANGES_FILE
    exchanges = pd.read_csv(exchanges_file, index_col=0)['Name'] if exchanges_file in os.listdir() else []
    setup_crypto_db()
    setup_fx_db()
    setup_exchanges_db()
    print('done')



def check_watchlists_and_portfolios():
    users = User.objects.all()
    for user in users:
        if not Watchlist.objects.filter(user=user).exists():
            new_watchlist = Watchlist.objects.create(user=user)
            new_watchlist.save()




def all_db_checks():

    pass

