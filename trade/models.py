from django.db import models

# Create your models here.


class SavedExchanges(models.Model):
    user = models.ForeignKey('website.UserProfile', on_delete=models.CASCADE, related_name='savedexchanges_userprofile')
    exchange = models.ForeignKey('crypto.Exchange', on_delete=models.CASCADE, related_name='savedexchanges_exchange')

