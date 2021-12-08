from django.db import models

# Create your models here.
from django.db import models
import datetime


# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey('website.UserProfile', related_name='message_sender', on_delete=models.CASCADE,
                               unique=False)
    recipient = models.ForeignKey('website.UserProfile', related_name='message_recipient', on_delete=models.CASCADE,
                                  unique=False)
    content = models.TextField(max_length=1000, blank=False)
    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.timestamp) + ' ' + self.sender.user.username + ': ' + str(self.content)


