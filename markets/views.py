from django.conf import settings
from utils.crypto_monitor import *
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
import datetime
from .forms import AddFXTicker
from utils.fx_monitor import *
from utils.portfolio_value import get_portfolio_value
from website.models import UserProfile
from markets.models import Currency
# Create your views here.


def markets(request):
    context={}


    return render(request, 'markets/markets.html', context)


def crypto(request):
    context = {}

    return render(request, 'markets/crypto.html', context)


def forex(request):

    if request.method == 'GET':
        print('get')
        print(request.GET)
        if 'currency' in str(request.GET):
            currency = request.GET['currency']
        elif request.user.is_authenticated and UserProfile.objects.filter(user=request.user).currency.exists():
            currency = UserProfile.objects.filter(user=request.user).first().currency.symbol
        else:
            currency = settings.DEFAULT_CURRENCY

        rates = pd.DataFrame(get_rates(currency))[1:]
        print(SORTED_CURRENCIES)
        rates.columns = [currency]
        context = {'currency': currency, 'currencies': SORTED_CURRENCIES, 'rates': rates.to_html(), 'add_ticker': AddFXTicker()}
        return render(request, 'markets/forex.html', context)

    elif request.method == 'POST':
        if 'add_ticker' in str(request.POST):
            form = AddFXTicker(request.POST)
            if form.is_valid():
                form_data = form.cleaned_data



def forex_matrix(request):
    table = get_forex_matrix()
    context = {'currencies': SORTED_CURRENCIES, 'table': table.to_html()}
    return render(request, 'markets/forex_matrix.html', context)

def indices(request):
    context = {}

    return render(request, 'markets/indices.html', context)

def stocks(request):
    context = {}

    return render(request, 'markets/stocks.html', context)

def bonds(request):
    context = {}

    return render(request, 'markets/bonds.html', context)

def commodities(request):
    context = {}

    return render(request, 'markets/commodities.html', context)


def trends(request):
    context = {}
    filename = settings.CRYPTO_FILE

    coins = pd.read_csv(filename, index_col=0).iloc[:, :8]
    coins.loc[:, 'Price'] = coins.loc[:, 'Price'].astype('float64').round(6)
    print(coins.columns)

    if request.method == 'GET':

        timeframe = request.GET['timeframe'] if 'timeframe' in str(request.GET) else '24h'
        print(f'timeframe {timeframe}')
        timeframes = ['1h', '24h']
        timeframes.remove(timeframe)
        timeframes.insert(0, timeframe)
        context['timeframes'] = timeframes

        sort_key = timeframe + ' Δ'

        gainers = coins.sort_values(by=sort_key, ascending=False)
        losers = coins.sort_values(by=sort_key, ascending=True)

        print(coins.columns[4])

        gainers = prepare_df_display(gainers, cols_to_split=[2, 5, 6], upd_col=False, round_decimals=4)
        losers = prepare_df_display(losers, cols_to_split=[2, 5, 6], upd_col=False, round_decimals=4)

        context['gainers_table'] = gainers.to_html(justify='center', escape=False)
        context['losers_table'] = losers.to_html(justify='center', escape=False)

        return render(request, 'markets/trends.html', context)

    elif request.method == 'POST':
        pass
        return render(request, 'markets/trends.html', context)



