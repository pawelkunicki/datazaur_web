from django.test import TestCase
from .models import Cryptocurrency, Exchange
from .views import *



class CryptoTest(TestCase):

    def create_object(self, name='test_coin', symbol='tst'):
        return Cryptocurrency.objects.create(name=name, symbol=symbol)

    def test_crypto(self):
        coin = self.create_object()
        self.assertTrue(isinstance(coin, Cryptocurrency))
        self.assertEqual(coin.name, 'test_coin')

