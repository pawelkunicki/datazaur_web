from django.db import models

from django.contrib.auth.models import User

#from watchlist.models import Watchlist
#from portfolio.models import Portfolio
# Create your models here.




class Currency(models.Model):
    name = models.CharField(max_length=32, unique=False, null=True)
    symbol = models.CharField(max_length=3, unique=True, null=False)
    country = models.CharField(max_length=32, blank=True, null=True)
    cross_rates = models.ManyToManyField('forex.Currency', related_name='currency_cross_rates', through='crossrate',
                                         through_fields=('base_currency', 'quote_currency'), blank=True)




