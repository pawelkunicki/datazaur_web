
NAVBAR_SUFFIX_AUTHED = (
                ("Account", "{% static 'website/account.html' %}"),
                ("Log Out", "{% static 'website/logout.html' %}"),
                )

NAVBAR_SUFFIX_UNAUTHED = (
                ("Log In", "{% static 'website/login.html' %}"),
                ("Sign Up", "{% static 'website/signup.html' %}"),
                )

MAIN_NAVBAR = (
               ("Home", "{% static 'website/home.html' %}"),
               ("Markets", "{% static 'markets/markets.html' %}"),
               ("Trade", "{% static 'trade/trade.html' %}"),
               ("Watchlist", "{% static watchlist/watchlist.html' %}"),
               ("Trends", "{% static 'markets/trends.html' %}"),
               ("News", "{% static 'news/news.html' %}"),
               ("Macro", "{% static 'macro/macro.html' %}"),
               ("Calendar", "{% static 'macro/calendar.html' %}"),
               ("Messenger", "{% static 'messenger/messenger.html' %}"),
               ("Social Trading", "{% static 'social/social.html' %}"),
               ("Highscores", "{% static 'social/highscores.html' %}"),
               ("Downloads", "{% static 'website/downloads.html' %}"),
                )


NAVBAR_MARKETS = (
               ("Home", "{% static 'website/home.html' %}"),
               ("Crypto", "{% static 'crypto/crypto.html' %}"),
               ("Forex", "{% static 'markets/forex.html' %}"),
               ("Indices", "{% static markets/indices.html' %}"),
               ("Bonds", "{% static 'markets/bonds.html' %}"),
               ("Commodities", "{% static 'markets/commodities.html' %}"),
               ("Stocks", "{% static 'markets/stocks.html' %}"),
               ("Funds", "{% static 'markets/funds.html' %}"),
               ("ETFs", "{% static 'markets/etfs.html' %}"),
               ("Watchlist", "{% static 'watchlist/watchlist.html' %}"),
               ("Trends", "{% static 'markets/trends.html' %}"),
               ("Trade", "{% static 'trade/trade.html' %}"),
               ("Social Trading", "{% static 'social/social.html' %}"),
               ("Highscores", "{% static 'social/highscores.html' %}"),
                )


NAVBAR_TRADE = (
               ("Home", "{% static 'website/home.html' %}"),
               ("Cointegration", "{% static 'trade/cointegration.html' %}"),
               ("Momentum", "{% static 'trade/momentum.html' %}"),
               ("Arbitrage", "{% static 'trade/arbitrage.html' %}"),
               ("Twitter", "{% static 'trade/twitter.html' %}"),
               ("Social Trading", "{% static markets/indices.html' %}"),
               ("Highscores", "{% static 'social/highscores.html' %}"),
               ("Trends", "{% static 'markets/trends.html' %}"),
               ("Messenger", "{% static 'messenger/messenger.html' %}"),
               ("Watchlist", "{% static 'watchlist/watchlist.html' %}"),
                )

