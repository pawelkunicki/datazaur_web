from django.shortcuts import render
from django.conf import settings
from .forms import TradeForm
from .models import SavedExchanges
from website.models import UserProfile
from crypto.models import Exchange, ExchangeCoins

# Create your views here.


def trade(request):
    context = {}
    context['sidebar_items'] = zip(('Algorithms', 'Arbitrage', 'History'), ('algorithms', 'arbitrage', 'history'))
    context['trade_form'] = TradeForm()
    context['exchanges'] = Exchange.objects.all()


    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        currency = profile.currency if profile.currency else settings.DEFAULT_CURRENCY

        context['connected_exchanges'] = SavedExchanges.objects.filter(user=profile)
        print(context['connected_exchanges'])

    else:
        currency = settings.DEFAULT_CURRENCY

    context['currency'] = currency


    if request.method == 'GET':
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

        elif 'connect' in str(request.POST):
            print(request.POST)
            exchange = Exchange.objects.get(id=request.POST['exchange_input'])
            if SavedExchanges.objects.filter(user=profile, exchange=exchange).exists():
                pass
            else:
                SavedExchanges.objects.create(user=profile, exchange=exchange).save()

                print(f'saved exchange: {exchange}')

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



