import ccxt
import pandas as pd
import re


def watchlist_prices(watchlist):
    quote_curr = watchlist.currency.symbol

    source = watchlist.default_source.name.lower()
    exchange = getattr(ccxt, source)({'enableRateLimit': True})
    coins = watchlist.coins.all()
    rdy_coins = list(filter(lambda x: x.symbol.upper() in exchange.codes, coins))

    tickers = [f'{coin.symbol.upper()}/{quote_curr}' for coin in rdy_coins]

    markets = pd.DataFrame(exchange.load_markets()).transpose()
    ready_tickers = []
    for ticker in tickers:
        if ticker in markets.index:
            ready_tickers.append(ticker)
        #elif ticker.split()




    print(markets)
    print(list(watchlist.coins.all()))


    print(tickers)
    try:
        prices = exchange.fetch_tickers(tickers)
        print(prices)
        if not prices:
            tickers = []
        return prices

    except Exception as e:
        print(f'error {e}')










