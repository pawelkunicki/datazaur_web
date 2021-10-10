from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from markets.models import Currency
from watchlist.models import Watchlist
#from portfolio.models import Portfolio
# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey('auth.User', related_name='userprofile_user', on_delete=models.CASCADE)
    currency = models.ForeignKey('markets.Currency', on_delete=models.CASCADE, related_name='myuser_currency', null=True,
                                 blank=True)
    portfolio = models.ForeignKey('watchlist.Portfolio', related_name='userprofile_portfolio', on_delete=models.CASCADE, null=True, blank=True)
    watchlist = models.ForeignKey('watchlist.Watchlist', related_name='userprofile_watchlist', on_delete=models.CASCADE, null=True, blank=True)
    email = models.CharField(max_length=32, null=True, blank=True)
    exchanges = models.ManyToManyField('crypto.Exchange', related_name='userprofile_exchanges')
    friends = models.ManyToManyField('self', related_name='userprofile_friends')
    #online = models.BooleanField(default=False)
    #last_login = models.IntegerField(default=0)


class FriendLists(models.Model):
    user = models.ForeignKey('website.UserProfile', related_name='friendlists_user', on_delete=models.CASCADE, null=False)
    friend = models.ForeignKey('website.UserProfile', related_name='friendlists_friend', on_delete=models.CASCADE, null=False)

