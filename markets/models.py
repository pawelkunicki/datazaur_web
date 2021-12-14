from django.db import models

from django.contrib.auth.models import User


class Currency(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, unique=False, null=True)
    symbol = models.CharField(max_length=3, unique=True, null=False)
    country = models.CharField(max_length=32, blank=True, null=True)







