import pandas as pd
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .forms import AddToPortfolio, ChangeCurrency, NewWatchlist, SetSource, AddCoin
from .models import Watchlist, Portfolio, Amounts
from markets.models import Currency
from crypto.models import Cryptocurrency, Exchange
from utils.portfolio_value import get_portfolio_value
from utils.watchlist_prices import watchlist_prices
from website.models import UserProfile


@login_required
def watchlist(request):
    profile = UserProfile.objects.get(user=request.user)
    portfolio = Portfolio.objects.get(user=profile)
    watchlists = Watchlist.objects.filter(user=profile)
    watchlist = watchlists.first()
    coins = Cryptocurrency.objects.all()
    watchlist_coins = watchlist.coins.all()
    #prices = watchlist_prices(watchlist)


    context = {'watchlists': watchlists, 'currency': portfolio.currency, 'coins': coins, 'watchlist_coins': watchlist_coins,
               'new_watchlist': NewWatchlist(), 'change_currency': ChangeCurrency(), 'set_source': SetSource(),
               'add_form': AddToPortfolio()}

    if request.method == 'GET':
        return render(request, 'watchlist/watchlist.html', context)


    elif request.method == 'POST':
        if 'add_coin' in str(request.POST):
            print('addin')
            watchlist.coins.add(Cryptocurrency.objects.get(symbol=request.POST['selected_coin']))
            watchlist.save()

        elif 'delete' in str(request.POST):
            ids_to_delete = [x.split('_')[1] for x in request.POST['checked_symbols'].split(',')]
            for id in ids_to_delete:
                watchlist.coins.remove(Cryptocurrency.objects.get(id=id))

        elif 'change_currency' in str(request.POST):
            print(request.POST)
            chg_form = ChangeCurrency(request.POST)
            if chg_form.is_valid():
                data = chg_form.cleaned_data
                new_currency = Currency.objects.get(id=data['currency'])
                portfolio.currency = new_currency
                portfolio.save()
            else:
                print(f'errors: {chg_form.errors}')

        elif 'add_to_portfolio' in str(request.POST):
            print('addin')
            add_form = AddToPortfolio(request.POST)
            if add_form.is_valid():
                data = add_form.cleaned_data
                coin = data['coin']
                amount = data['amount']
                if Amounts.objects.filter(portfolio=portfolio).filter(coin=coin).exists():
                    amount_obj = Amounts.objects.filter(portfolio=portfolio).filter(coin=coin)
                    amount_obj.amount += amount
                    amount_obj.save()
                else:
                    new_amount = Amounts.objects.create(portfolio=portfolio, coin=coin, amount=amount)
                    new_amount.save()
            else:
                print(f'errors: {add_form.errors}')

        elif 'new_watchlist' in str(request.POST):
            print('new_watch')
            print(request.POST)

            watchlist_form = NewWatchlist(request.POST)
            if watchlist_form.is_valid():
                form_data = watchlist_form.cleaned_data
                currency = Currency.objects.get(symbol=form_data['currency'])
                if form_data['type'] == 'Watchlist':
                    Watchlist.objects.create(user=profile, currency=currency)
                elif form_data['type'] == 'Portfolio':
                    Portfolio.objects.create(user=profile, currency=currency)

        elif 'source' in str(request.POST):
            print('set source')
            print(request.POST)
            source_form = SetSource(request.POST)
            if source_form.is_valid():
                form_data = source_form.cleaned_data
                exchange = Exchange.objects.get(id=form_data['source'])
                watch_coin = watchlist.coins.objects.get(id=form_data['coin'])
                watch_coin.source = exchange
                watch_coin.save()
                print(f'source changed to {form_data["source"]}')
            else:
                print(f'errors: {source_form.errors}')

        return HttpResponseRedirect(reverse('watchlist:watchlist', args=()))




