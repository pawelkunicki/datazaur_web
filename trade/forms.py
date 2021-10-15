from django import forms
from static.data.constants import ORDER_TYPES, MARKET_TYPES
from crypto.models import Cryptocurrency
from markets.models import Currency
import ccxt
from crypto.models import Exchange, ExchangeCoins


class TradeForm(forms.Form):
    exchange = forms.ChoiceField(label='Exchange', choices=enumerate(ccxt.exchanges))
    ticker = forms.ChoiceField(label='Coin', choices=())
    amount = forms.FloatField(label='Amount')
    price = forms.FloatField(label='Price')
    order_type = forms.ChoiceField(label='Order type', choices=enumerate(ORDER_TYPES))
    market = forms.ChoiceField(label='Market', choices=enumerate(MARKET_TYPES))


class ConnectForm(forms.Form):
    exchange = forms.ChoiceField(label='Exchange', choices=enumerate(ccxt.exchanges))



class FindQuote(forms.Form):
    ticker = forms.ChoiceField(label='Coin', choices=())
    currency = forms.ChoiceField(label='Currency', choices=())
    exchange = forms.ChoiceField(label='Exchange', choices=enumerate(ccxt.exchanges))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ticker'].choices = [(coin.id, coin.name) for coin in Cryptocurrency.objects.all()]
        self.fields['currency'].choices = [(curr.id, curr.name) for curr in Currency.objects.all()]
