from .models import Watchlist
from django import forms
from markets.models import Currency
from crypto.models import Cryptocurrency


class AddCoin(forms.Form):
    coin = forms.ChoiceField(label='Coin', choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['coin'].choices = [(c.id, c.name) for c in Cryptocurrency.objects.all()]
        except Exception as e:
            print(f'error: {e}')


class ChangeCurrency(forms.Form):
    currency = forms.ChoiceField(label='Currency', choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['currency'].choices = [(c.id, c.name) for c in Currency.objects.all()]
        except Exception as e:
            print(f'error: {e}')


class NewWatchlist(forms.Form):
    name = forms.CharField(label='Name', max_length=16)
    type = forms.ChoiceField(label='Type', choices=((1, 'Watchlist'), (2, 'Portfolio')))
    base_currency = forms.ChoiceField(label='Currency')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['base_currency'].choices = [(c.symbol, c.name) for c in Currency.objects.all()]



class AddToPortfolio(forms.Form):
    coin = forms.ChoiceField(label='Coin', required=True)
    amount = forms.FloatField(label='Amount', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['coin'].choices = [(c.id, c.name) for c in Cryptocurrency.objects.all()]