from django.db import models

from django.contrib.auth.models import User
from forex.models import Currency
#from watchlist.models import Watchlist
#from portfolio.models import Portfolio
# Create your models here.


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=32, blank=False)
    symbol = models.CharField(max_length=8, blank=False)
    description = models.TextField(max_length=256)
    url = models.CharField(max_length=32, blank=True, null=True)
    algorithm = models.CharField(max_length=32)
    proof_type = models.CharField(max_length=32)
    total_coins_mined = models.FloatField(blank=True, null=True)
    circulating_supply = models.FloatField(blank=True, null=True)
    max_supply = models.FloatField(blank=True, null=True)
    used_in_defi = models.BooleanField(blank=True, null=True)
    used_in_nft = models.BooleanField(blank=True, null=True)
    block_reward = models.FloatField(blank=True, null=True)

    #watchlist = models.ManyToManyField(Watchlist, related_name='cryptocurrency_watchlist', blank=True)


class Exchange(models.Model):

    class Grade(models.TextChoices):
        A = 'A', ('A')
        B = 'B', ('B')
        C = 'C', ('C')
        NA = 'NA', ('NA')

    name = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    grade = models.CharField(choices=Grade.choices, max_length=3, default=Grade.NA)
    url = models.CharField(max_length=32, default='')
    volume = models.FloatField(default=0)
    coins = models.ManyToManyField('crypto.Cryptocurrency', related_name='exchange_coins', blank=True)

#through='exchangecoins',  through_fields=('exchange', 'coin')


class ExchangeCoins(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='exchangecoins_exchange')
    coin = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, related_name='exchangecoins_coin')


class Ticker(models.Model):
    base_currency = models.ForeignKey('crypto.Cryptocurrency', on_delete=models.CASCADE)
    quote_currency = models.ForeignKey('forex.Currency', on_delete=models.CASCADE)
    source = models.ForeignKey('crypto.Exchange', on_delete=models.CASCADE)
    bid_price = models.FloatField(default=0)
    ask_price = models.FloatField(default=0)


    hourly_change = models.FloatField(default=0)
    daily_change = models.FloatField(default=0)
    weekly_change = models.FloatField(default=0)
    monthly_change = models.FloatField(default=0)

class Currency(models.Model):
    name = models.CharField(max_length=32, unique=False, null=True)
    symbol = models.CharField(max_length=3, unique=True, null=False)
    country = models.CharField(max_length=32, blank=True, null=True)
    cross_rates = models.ManyToManyField('forex.Currency', related_name='currency_cross_rates', through='crossrate',
                                         through_fields=('base_currency', 'quote_currency'), blank=True)




class Portfolio(models.Model):
    user = models.ForeignKey('website.UserProfile', on_delete=models.CASCADE, related_name='portfolio_userprofile')
    currency = models.ForeignKey('forex.Currency', on_delete=models.CASCADE, related_name='portfolio_currency',
                                 blank=True, null=True)
    coins = models.ManyToManyField('crypto.Cryptocurrency', blank=True, related_name='portfolio_cryptocurrency',
                                   through='amounts', through_fields=('portfolio', 'coin'))



class Amounts(models.Model):
    portfolio = models.ForeignKey('portfolio.Portfolio', on_delete=models.CASCADE, related_name='amounts_portfolio')
    coin = models.ForeignKey('crypto.Cryptocurrency', on_delete=models.CASCADE, related_name='amounts_coin')
    amount = models.FloatField()



class Watchlist(models.Model):
    user = models.ForeignKey('website.UserProfile', blank=False, null=False, related_name='watchlist_userprofile', on_delete=models.CASCADE)
    currency = models.ForeignKey('forex.Currency', blank=True, null=True, related_name='watchlist_currency',
                                 on_delete=models.CASCADE)
    coins = models.ManyToManyField('crypto.Cryptocurrency', blank=True, related_name='watchlist_cryptocurrency',
                                    through='watchlistcoins', through_fields=('watchlist', 'coin'))



class WatchlistCoins(models.Model):
    watchlist = models.ForeignKey('watchlist.Watchlist', on_delete=models.CASCADE, related_name='watchlistcoins_watchlist')
    coin = models.ForeignKey('crypto.Cryptocurrency', on_delete=models.CASCADE, related_name='watchlistcoins_cryptocurrency')
