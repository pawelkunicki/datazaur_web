from django.shortcuts import render
from .forms import AddFXTicker
from utils.market_data import *
from website.models import UserProfile


# Create your views here.



def markets(request):
    context = {}


    #rates_df = get_fx_rates(settings.DEFAULT_CURRENCY)

    #coins_df = coins_by_mcap().iloc[:20, [1, 2, 4]]

    # indices_df = get_indices_table()
    # indices_df['24h Δ'] = indices_df['24h Δ'].apply(color_cell)
    #
    # bonds_df = get_bonds_table('10Y')
    # bonds_df['24h Δ'] = bonds_df['24h Δ'].apply(color_cell)
    #
    # commodities_df = get_commodities()

    context = all_markets_data(600)

    print(context)
    context['currencies'] = settings.SORTED_CURRENCIES


    # context['indices'] = indices_df.to_html(escape=False)
    # context['forex'] = rates_df.to_html(escape=False)
    # context['coins'] = coins_df.to_html(escape=False)
    # context['yields'] = bonds_df.to_html(escape=False)
    # context['commodities'] = commodities_df.to_html(escape=False)


    # price_headers = ('Instrument', 'Price', '24h Δ')
    # context['headers'] = {'indices': price_headers, 'currencies': price_headers, 'coins': price_headers,
    #                       'commodities': ('Name', 'Price', '24h Δ'), 'stocks': price_headers, 'funds': price_headers,
    #                       'etfs': price_headers, 'bonds': ('Bond', 'Yield', '24h Δ')}


    return render(request, 'markets/markets.html', context)



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

        rates_df = pd.DataFrame(get_fx_rates(currency))
        col_name = rates_df.columns[0]
        rates_df = rates_df[rates_df[col_name] != 1]
        rates = [(i, v[col_name]) for i, v in rates_df.iterrows()]

        currencies = list(rates_df.index.values)
        if currency in currencies:
            currencies.remove(currency)
        currencies.insert(0, currency)
        context = {'currencies': currencies, 'rates': rates, 'add_ticker': AddFXTicker()}
        return render(request, 'markets/forex.html', context)

    elif request.method == 'POST':
        if 'add_ticker' in str(request.POST):
            form = AddFXTicker(request.POST)
            if form.is_valid():
                form_data = form.cleaned_data



def forex_matrix(request):
    table = get_fx_rates(settings.DEFAULT_CURRENCY)
    context = {'currencies': settings.SORTED_CURRENCIES, 'table': table.to_html()}
    return render(request, 'markets/forex_matrix.html', context)

def indices(request):
    context = {}

    return render(request, 'markets/indices.html', context)

def screener(request):
    context = {}

    return render(request, 'markets/screener.html', context)

def stocks(request):
    context = {}

    return render(request, 'markets/stocks.html', context)

def bonds(request):
    context = {}

    return render(request, 'markets/bonds.html', context)

def yield_curves(request):
    context = {}
    if request.method == 'GET' and 'country' in str(request.GET):
        country = request.GET['country']
    else:
        country = 'United States'



    context['main_curve'] = investpy.get_bonds_overview(country)
    context['yield_curves'] = get_yield_curves()
    print(context)
    return render(request, 'markets/yield_curves.html', context)


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



def funds(request):
    context = {}


    return render(request, 'markets/funds.html', context)




def etfs(request):
    context = {}


    return render(request, 'markets/etfs.html', context)



















