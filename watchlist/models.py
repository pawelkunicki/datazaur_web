from django.db import models

# Create your models here.


class Portfolio(models.Model):
    user = models.ForeignKey('website.UserProfile', on_delete=models.CASCADE, related_name='portfolio_userprofile')
    name = models.CharField(max_length=32, default='portfolio')
    currency = models.ForeignKey('markets.Currency', on_delete=models.CASCADE, related_name='portfolio_currency',
                                 blank=True, null=True)
    coins = models.ManyToManyField('crypto.Cryptocurrency', blank=True, related_name='portfolio_cryptocurrency',
                                   through='amounts', through_fields=('portfolio', 'coin'))



class Amounts(models.Model):
    portfolio = models.ForeignKey('watchlist.Portfolio', on_delete=models.CASCADE, related_name='amounts_portfolio')
    coin = models.ForeignKey('crypto.Cryptocurrency', on_delete=models.CASCADE, related_name='amounts_coin')
    amount = models.FloatField(default=0)



class Watchlist(models.Model):
    user = models.ForeignKey('website.UserProfile', blank=False, null=False, related_name='watchlist_userprofile',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=32, default='watchlist')
    currency = models.ForeignKey('markets.Currency', blank=True, null=True, related_name='watchlist_currency',
                                 on_delete=models.CASCADE)
    default_source = models.ForeignKey('crypto.Exchange', on_delete=models.CASCADE, null=True, blank=True)
    coins = models.ManyToManyField('crypto.Cryptocurrency', blank=True, related_name='watchlist_watchlistcoins')





