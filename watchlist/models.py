from django.db import models

# Create your models here.


class Portfolio(models.Model):
    user = models.ForeignKey('website.UserProfile', on_delete=models.CASCADE, related_name='portfolio_userprofile')
    currency = models.ForeignKey('markets.Currency', on_delete=models.CASCADE, related_name='portfolio_currency',
                                 blank=True, null=True)
    coins = models.ManyToManyField('crypto.Cryptocurrency', blank=True, related_name='portfolio_cryptocurrency',
                                   through='amounts', through_fields=('portfolio', 'coin'))



class Amounts(models.Model):
    portfolio = models.ForeignKey('watchlist.Portfolio', on_delete=models.CASCADE, related_name='amounts_portfolio')
    coin = models.ForeignKey('crypto.Cryptocurrency', on_delete=models.CASCADE, related_name='amounts_coin')
    amount = models.FloatField()



class Watchlist(models.Model):
    user = models.ForeignKey('website.UserProfile', blank=False, null=False, related_name='watchlist_userprofile', on_delete=models.CASCADE)
    currency = models.ForeignKey('markets.Currency', blank=True, null=True, related_name='watchlist_currency',
                                 on_delete=models.CASCADE)
    coins = models.ManyToManyField('crypto.Cryptocurrency', null=True, blank=True, related_name='watchlist_cryptocurrency',
                                   through='watchlist.Watchlistcoins', through_fields=('watchlist', 'coin'))



class WatchlistCoins(models.Model):
    watchlist = models.ForeignKey('watchlist.Watchlist', on_delete=models.CASCADE, related_name='watchlistcoins_watchlist')
    coin = models.ForeignKey('crypto.Cryptocurrency', on_delete=models.CASCADE, related_name='watchlistcoins_cryptocurrency')


