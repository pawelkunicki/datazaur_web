from django.db import models

# Create your models here.


class Cryptocurrency(models.Model):
    coin_id = models.CharField(max_length=32, blank=False)
    symbol = models.CharField(max_length=8, blank=False)
    name = models.CharField(max_length=32, blank=False)
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
    quote_currency = models.ForeignKey('markets.Currency', on_delete=models.CASCADE)
    source = models.ForeignKey('crypto.Exchange', on_delete=models.CASCADE)
    bid_price = models.FloatField(default=0)
    ask_price = models.FloatField(default=0)

    hourly_change = models.FloatField(default=0)
    daily_change = models.FloatField(default=0)
    weekly_change = models.FloatField(default=0)
    monthly_change = models.FloatField(default=0)

