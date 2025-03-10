
from django.shortcuts import render
from django.conf import settings
from .forms import TradeForm, FindQuote, ConnectForm
from .models import SavedExchanges
from website.models import UserProfile
from crypto.models import Exchange
from utils.charts import Chart
from utils.count_tweets import *
from utils.random_color import *
from utils.formatting import *
import ccxt
import numpy as np
import pandas as pd
# Create your views here.


def trade(request):
    context = {}
    context['sidebar_items'] = zip(('Algorithms', 'Arbitrage', 'History'), ('algorithms', 'arbitrage', 'history'))
    context['trade_form'] = TradeForm()
    context['exchanges'] = Exchange.objects.all()
    context['conn_form'] = ConnectForm()

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        currency = profile.currency if profile.currency else settings.DEFAULT_CURRENCY

        context['connected_exchanges'] = SavedExchanges.objects.filter(user=profile)
        print(context['connected_exchanges'])

    else:
        currency = settings.DEFAULT_CURRENCY

    context['currency'] = currency


    if request.method == 'GET':
        print(request.GET)
        if 'exchange' in str(request.GET):
            exchange = getattr(ccxt, Exchange.objects.get(id=request.GET['exchange']).name)()
            markets = pd.DataFrame(exchange.fetch_tickers()).transpose()[['last', 'percentage', 'quoteVolume']]
            markets.columns = ['Price', '24h Δ', 'volume']
            markets = prepare_df_display(markets)
            context['markets'] = markets.to_html(escape=False, justify='center')


        context['ticker'] = request.GET['ticker'] if 'ticker' in str(request.GET) else None


    elif request.method == 'POST':
        if 'buy' in str(request.POST):
            context['ticker'] = request.POST['ticker']
            buy_form = TradeForm(request.POST)
            if buy_form.is_valid():
                buy_data = buy_form.cleaned_data
                # execute buy offer
            else:
                print(f'errors: {buy_form.errors}')
        elif 'sell' in str(request.POST):
            context['ticker'] = request.POST['ticker']
            sell_form = TradeForm(request.POST)
            if sell_form.is_valid():
                sell_data = sell_form.cleaned_data
                # sell offer
            else:
                print(f'errors: {sell_form.errors}')

        elif request.user.is_authenticated and 'connect' in str(request.POST):
            print(request.POST)
            conn_form = ConnectForm(request.POST)
            if conn_form.is_valid():
                form_data = conn_form.cleaned_data
                exchange = Exchange.objects.get(id=form_data['exchange'])
                if SavedExchanges.objects.filter(user=profile, exchange=exchange).exists():
                    pass
                else:
                    SavedExchanges.objects.create(user=profile, exchange=exchange).save()
                    print(f'saved exchange: {exchange}')
            else:
                print(conn_form.errors)

            context['conn_exchanges'] = SavedExchanges.objects.filter(user=profile)
            return render(request, 'trade/trade.html', context)

        elif 'disconnect' in str(request.POST):
            exchange = Exchange.objects.get(id=request.POST['exchange_input'])
            if SavedExchanges.objects.filter(user=profile).filter(exchange=exchange).exists():
                SavedExchanges.objects.filter(user=profile).filter(exchange=exchange).delete()
                print(f'disconnected from: {exchange}')
            else:

                print(f'{exchange} wasnt connected')



    return render(request, 'trade/trade.html', context)


def algorithms(request):
    context = {}


    return render(request, 'trade/algorithms.html', context)

def cointegration(request):
    context = {}
    if request.user.is_authenticated:
        profile = request.user.profile
        context['connected_exchanges'] = SavedExchanges.objects.filter(user=profile)


    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        pass

    return render(request, 'trading/algorithms.html', context)


def momentum(request):
    context = {}
    context['find_quote'] = FindQuote()
    if request.method == 'GET':

        return render(request, 'trade/momentum.html', context)

    elif request.method == 'POST':


        pass

def arbitrage(request):
    context = {}

    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        pass

    return render(request, 'trading/arbitrage.html', context)



def history(request):
    context = {}

    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        pass

    return render(request, 'trading/history.html', context)



def twitter(request):
    context = {'info': {'query': ''}}
    print(request.GET)
    if request.method == 'GET' and 'query' in str(request.GET):
        symbol = request.GET['search_query']
        granularity = request.GET['granularity']
        query = {'query': symbol, 'granularity': granularity}
        table, since = tweet_count(query)
        context['table'] = table.to_html(escape=False, justify='center')
        context['info'] = {'query': query['query'],
                           'start_date': table.loc[0, 'start'],
                           'end_date': table['end'].values[-1],
                           'total_count': sum(table['tweet_count'])}

        intervals = {'hour': '1h', 'minute': '1m', 'day': '1d'}
        interval = intervals[granularity.lower()]
        exchange = settings.DEFAULT_EXCHANGE
        currency = settings.DEFAULT_CURRENCY
        ticker = symbol.replace('#', '').upper() + '/' + currency + 'T'
        prices = get_prices(ticker, exchange, interval, since)
        prices[0] = prices[0].apply(lambda x: ccxt.Exchange.iso8601(x)[:16].replace('T', ' '))
        prices.columns = ['start', 'Open', 'High', 'Low', 'Close', 'Volume']

        joined_table = table.set_index('start').join(prices.set_index('start')).dropna()
        #joined_table['tweet_delta'] = 100 * (joined_table['tweet_count'] - joined_table['tweet_count'].shift()) / joined_table['tweet_count'].shift()
        #joined_table['close_delta'] = 100 * (joined_table['Close'] - joined_table['Open']) / joined_table['Open']
        joined_table['tweet_delta'] = np.log(joined_table['tweet_count'] / joined_table['tweet_count'].shift())
        joined_table['close_delta'] = np.log(joined_table['Close'] / joined_table['Close'].shift())

        context['corr'] = get_corr_matrix(joined_table.iloc[:, 1:]).to_html(escape=False, justify='center')
        context['joined_table'] = joined_table.to_html(escape=False, justify='center')


        df = joined_table[['tweet_delta', 'close_delta']]
        PALETTE = [get_random_color() for col in df.columns]

        chart = Chart('line', chart_id='tweets_price', palette=PALETTE)
        chart.from_df(df, values=['close_delta', 'tweet_delta'], labels='start')
        js_scripts = chart.get_js()
        context['charts'] = []
        context['charts'].append(chart.get_presentation())
        context['table'] = chart.get_html()
        context['js_scripts'] = js_scripts


    return render(request, 'trade/twitter.html', context)



