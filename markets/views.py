from django.shortcuts import render
from .forms import AddFXTicker
from utils.market_data import *
from website.models import UserProfile


def markets(request):
    context = all_markets_data(600)
    context['currencies'] = settings.SORTED_CURRENCIES
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






def funds(request):
    context = {}


    return render(request, 'markets/funds.html', context)




def etfs(request):
    context = {}


    return render(request, 'markets/etfs.html', context)



















