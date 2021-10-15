import ccxt
import pycoingecko
from forex_python.converter import CurrencyRates
from .crypto_data import *
from utils.compare_timestamps import compare_timestamps
from crypto.models import Cryptocurrency
from django.conf import settings




def get_currency_value(base, quote, amount):
    rates = CurrencyRates()
    rate = rates.get_rate(base, quote)
    return amount * rate


def gecko_quote(base, quote):
    result = {}
    gecko = pycoingecko.CoinGeckoAPI()
    coin = Cryptocurrency.objects.filter(symbol=base).first().coin_id
    data = gecko.get_coin_by_id(coin)['market_data']
    result['coin'] = coin
    result['price'] = data['current_price'][quote]
    mcap = data['market_cap']
    daily_chg = data['price_change_percentage_24h']
    weekly_chg = data['price_change_percentage_7d']
    monthly_chg = data['price_change_percentage_30d']
    yearly_chg = data['price_change_percentage_1y']
    return coin, price, mcap, daily_chg, weekly_chg, monthly_chg, yearly_chg




def find_quote(base, quote, exchanges):
    ticker = base.upper() + '/' + quote.upper()
    for exchange_id in exchanges:
        exchange = getattr(ccxt, exchange_id)()
        markets = pd.DataFrame(exchange.load_markets()).transpose()
        if ticker in markets.index:
            return exchange.fetch_ticker(ticker)['last']
    return False


def get_crypto_value(coin, quote, amount):
    currency = settings.DEFAULT_CURRENCY
    coins = top_coins_by_mcap()

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



