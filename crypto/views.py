# Create your views here.
from django.shortcuts import render
from utils.crypto_data import *
from .models import Cryptocurrency
from utils.compare_timestamps import compare_timestamps
from utils.charts import Chart
from utils.random_color import get_random_color
from utils.crypto_data import exchanges_by_vol, top_coins_by_mcap

from utils.other_data import *
from utils.formatting import *
from watchlist.models import Watchlist, WatchlistCoins, Portfolio, Amounts
from watchlist.forms import AddCoin
from markets.models import Currency

from website.models import UserProfile

# Create your views here.

CRYPTO_FILE = settings.CRYPTO_FILE
EXCHANGES_FILE = settings.EXCHANGES_FILE


def crypto(request):
    context = {}
    context['currencies'] = Currency.objects.all()
    refresh_rate = settings.REFRESH_RATE
    coin_ids = []

    table = top_coins_by_mcap()
    table['Watchlist'] = table['Symbol'].apply(lambda
                                                   x: f"""<input type="checkbox" name="watch_{x}" id="watch_{x.split('</a>')[0].split('>')[1]}" class="star">""")
    table['Portfolio'] = table['Symbol'].apply(lambda
                                                   x: f""" <button type="submit" name="add_to_pf" value="{x.split('</a>')[0].split('>')[1]}"> Add </button>""")
    context['table'] = table.to_html(escape=False, justify='center')

    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user).first()
        watchlist = Watchlist.objects.filter(user=profile).first()
        coins = WatchlistCoins.objects.filter(watchlist=watchlist)

        print(coins)
        context['watchlist_ids'] = [c.coin.symbol.lower() for c in coins]
        print(context['watchlist_ids'])
        if profile.currency:
            context['currency'] = profile.currency.symbol
        else:
            context['currency'] = settings.DEFAULT_CURRENCY




    if request.method == 'POST' and not request.user.is_authenticated:
        return render(request, 'website/login_required.html', context)

    if request.method == 'POST' and 'amount' in str(request.POST):
        print('add to portfolio')
        print(request.POST)
        coin_id = request.POST['coin']
        new_amount = request.POST['amount']
        portfolio = Portfolio.objects.get(user=profile)
        if Amounts.objects.filter(portfolio=portfolio).filter(coin=coin_id).exists():
            amount = Amounts.objects.filter(portfolio=portfolio).filter(coin=coin_id)
            amount.amount += new_amount
            amount.save()
            print(f'added {amount} to {coin_id}')
        else:
            amount = Amounts.objects.create(portfolio=portfolio, coin=coin_id, amount=new_amount)
            amount.save()
            print(f'created {amount} of {coin_id}')

    if request.method == 'POST' and request.is_ajax and 'checked_symbols' in str(request.POST):
        print('ajax2')
        print(watchlist)
        print(watchlist.user)
        print(request.POST)


        symbols = request.POST['checked_symbols'].split(',')
        coin_ids = [symbol.split('_')[1].lower() for symbol in symbols if '_' in symbol]
        print(coin_ids)
        for symbol in coin_ids:
            if not Cryptocurrency.objects.filter(symbol=symbol).exists():
                print(f'coin {symbol} doesnt exist')
            else:
                coin = Cryptocurrency.objects.filter(symbol=symbol).first()
                print(coin)
                if not WatchlistCoins.objects.filter(watchlist=watchlist).filter(coin=coin).exists():
                    new_coin = WatchlistCoins.objects.create(watchlist=watchlist, coin=coin)
                    new_coin.save()
                    print(new_coin)
                    print(new_coin.coin)
        context['watchlist_ids'] = coin_ids

    print(context)
    return render(request, 'crypto/crypto.html', context)



def exchanges(request):
    table = None
    refresh_rate = 60
    if compare_timestamps(refresh_rate, EXCHANGES_FILE):
        table = pd.read_csv(EXCHANGES_FILE, index_col=0)
    else:
        table = exchanges_by_vol()
        table.to_csv(EXCHANGES_FILE)
    if request.method == 'POST':
        exchanges = request.POST['fav_exchanges']
    table['Favourite'] = ''
    context = {'table': table.to_html(justify='center', escape=False)}

    return render(request, 'crypto/exchanges.html', context)




def dominance(request):
    context = {}
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        if profile.currency:
            currency = profile.currency.symbol
    else:
        currency = settings.DEFAULT_CURRENCY
    top_n_choices = [10, 20, 50, 100]
    mcap_col = f'Market cap ({currency})'

    if request.method == 'GET':
        top_n_coins = int(request.GET['top_n_coins']) if 'top_n_coins' in str(request.GET) else 20
        top_n_choices.remove(top_n_coins)
        top_n_choices.insert(0, top_n_coins)
        PALETTE = [get_random_color() for i in range(top_n_coins)]
        df = pd.read_csv('crypto.csv', index_col=0).iloc[:top_n_coins][['Symbol', mcap_col]]
        df[mcap_col] = df[mcap_col].apply(lambda x: x.replace(',', ''))
        df['Dominance'] = df[mcap_col].apply(lambda x: 100 * float(x) / sum(df[mcap_col].astype('float64')))
        #df.loc[:, mcap_col] = list(map(lambda x: format(x, ','), df.loc[:, mcap_col]))
        chart = Chart('doughnut', chart_id='dominance_chart', palette=PALETTE)
        chart.from_df(df, values='Dominance', labels=list(df.loc[:, 'Symbol']))
        js_scripts = chart.get_js()
        context['charts'] = []
        context['charts'].append(chart.get_presentation())
        context['table'] = chart.get_html()
        context['js_scripts'] = js_scripts
        context['top_n_choices'] = top_n_choices

        return render(request, 'crypto/dominance.html', context)



def global_metrics(request):

    context = gecko_global_metrics()

    return render(request, 'crypto/global_metrics.html', context)


def events(request):
    context = {}

    return render(request, 'crypto/events.html', context)

def icos(request):
    context = {}

    return render(request, 'crypto/icos.html', context)


def nft(request):
    context = {}

    return render(request, 'crypto/ntf.html', context)


def defi(request):
    context = {}

    return render(request, 'crypto/defi.html', context)




def trends(request):
    context = {}
    filename = settings.CRYPTO_FILE

    if compare_timestamps(600, filename):
        coins = pd.read_csv(filename, index_col=0).iloc[:, :8]
    else:
        coins = top_coins_by_mcap().iloc[:, :8]

    coins.loc[:, 'Price'] = coins.loc[:, 'Price'].astype('float64').round(6)
    print(coins.columns)

    if request.method == 'GET':

        timeframe = request.GET['timeframe'] if 'timeframe' in str(request.GET) else '24h'

        timeframes = ['1h', '24h']
        timeframes.remove(timeframe)
        timeframes.insert(0, timeframe)
        context['timeframes'] = timeframes

        sort_key = timeframe + ' Δ'

        gainers = coins.sort_values(by=sort_key, ascending=False)
        losers = coins.sort_values(by=sort_key, ascending=True)


        gainers = prepare_df_display(gainers)
        losers = prepare_df_display(losers)

        context['gainers_table'] = gainers.to_html(justify='center', escape=False)
        context['losers_table'] = losers.to_html(justify='center', escape=False)

        return render(request, 'crypto/trends.html', context)

    elif request.method == 'POST':
        pass
        return render(request, 'crypto/trends.html', context)



def wallets(request):
    context = {}

    return render(request, 'crypto/wallets.html', context)


def games(request):
    context = {}

    return render(request, 'crypto/games.html', context)


