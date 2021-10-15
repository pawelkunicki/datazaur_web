import pycoingecko

api = pycoingecko.CoinGeckoAPI()

print(api.get_price('ETH', 'USD'))

