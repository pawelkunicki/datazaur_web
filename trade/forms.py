from django import forms
from static.data.constants import ORDER_TYPES, MARKET_TYPES
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

