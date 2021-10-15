from django.db import models

# Create your models here.


class Website(models.Model):
    user = models.ForeignKey('website.UserProfile', null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    selector = models.CharField(max_length=64)


