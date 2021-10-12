# Create your views here.
from django.shortcuts import render
from backup.crypto_monitor import *
from .models import Cryptocurrency
from utils.compare_timestamps import compare_timestamps
from utils.charts import Chart
from utils.random_color import get_random_color
from watchlist.models import Watchlist, WatchlistCoins, Portfolio, Amounts

from website.models import UserProfile

# Create your views here.

CRYPTO_FILE = settings.CRYPTO_FILE
EXCHANGES_FILE = settings.EXCHANGES_FILE

def crypto(request):
    context = {}
    refresh_rate = settings.REFRESH_RATE


    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        watchlist = Watchlist.objects.get(user=profile)
        coins = WatchlistCoins.objects.filter(watchlist=watchlist)
        context['watchlist_ids'] = [c.coin.symbol for c in coins]
        if profile.currency:
            context['currency'] = profile.currency.symbol
    else:
        context['currency'] = settings.DEFAULT_CURRENCY

    if CRYPTO_FILE not in os.listdir() or not compare_timestamps(refresh_rate, CRYPTO_FILE):
        table = coins_by_mcap()
    else:
        table = pd.read_csv(CRYPTO_FILE, index_col=0)
        table = prepare_df_display(table, cols_to_split=[2, 5, 6, 7], upd_col=True, round_decimals=3)

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
        print(request.POST)
        watchlist = Watchlist.objects.get(user=profile)
        WatchlistCoins.objects.filter(watchlist=watchlist).delete()
        symbols = request.POST['checked_symbols'].split(',')
        new_ids = []

        for symbol in symbols:
            if not Cryptocurrency.objects.filter(symbol=symbol).exists():
                pass
            else:
                coin = Cryptocurrency.objects.get(symbol=symbol)
                if not WatchlistCoins.objects.filter(watchlist=watchlist, coin=coin).exists():
                    coin_on_watchlist = WatchlistCoins.objects.create(watchlist=watchlist, coin=coin)
                    coin_on_watchlist.save()
                    new_ids.append(symbol)

        context['watchlist_ids'] = new_ids

    context['table'] = table.to_html(justify='center', escape=False)

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
        df['Dominance'] = df[mcap_col].apply(lambda x: float((100 * x)/sum(df[mcap_col])).__round__(4))
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

