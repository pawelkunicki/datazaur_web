import datetime
import os
from django.conf import settings
from forex.models import Currency

def add_cryptos_to_db():
    pass



def compare_timestamps(refresh_rate=60, file=None):
    now = datetime.datetime.now().timestamp()
    if file in os.listdir() and now - os.path.getmtime(file) < refresh_rate:
        return True
    else:
        return False



