import pandas as pd
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .forms import AddToPortfolio, ChangeCurrency, NewWatchlist, SetSource
from .models import Watchlist, WatchlistCoins, Portfolio, Amounts
from markets.models import Currency
from crypto.models import Cryptocurrency, Exchange, ExchangeCoins
from utils.portfolio_value import get_portfolio_value
from website.models import UserProfile


@login_required
def watchlist(request):
    context = {}
    profile = UserProfile.objects.get(user=request.user)
    print(profile)
    portfolio = Portfolio.objects.get(user=profile)
    watchlist = Watchlist.objects.get(user=profile)
    coins = Cryptocurrency.objects.all()
    currencies = Currency.objects.all()
    watchlist_coins = WatchlistCoins.objects.filter(watchlist=watchlist)
    coins_in_pf = Amounts.objects.filter(portfolio=portfolio)
    print(profile, portfolio, watchlist, watchlist_coins)
    context['new_watchlist'] = NewWatchlist()
    context['change_currency'] = ChangeCurrency()
    context['set_source'] = SetSource()



    if request.method == 'GET':
        print(watchlist_coins)
        context['watchlist_coins'] = watchlist_coins



    if request.method == 'POST' and 'add' in str(request.POST):
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
        return HttpResponseRedirect(reverse('watchlist:watchlist', args=()))

    elif request.method == 'POST' and 'currency' in str(request.POST):
        print(request.POST)
        chg_form = ChangeCurrency(request.POST)
        if chg_form.is_valid():
            data = chg_form.cleaned_data
            new_currency = Currency.objects.get(id=data['currency'])
            if portfolio.currency == new_currency:
                pass
            else:
                portfolio.currency = new_currency
                portfolio.save()
        else:
            print(f'errors: {chg_form.errors}')
        return HttpResponseRedirect(reverse('watchlist:watchlist', args=()))

    elif request.method == 'POST' and 'new_watchlist' in str(request.POST):
        print('new_watch')
        print(request.POST)

        watchlist_form = NewWatchlist(request.POST)
        if watchlist_form.is_valid():
            form_data = watchlist_form.cleaned_data
            currency = Currency.objects.get(symbol=form_data['currency'])
            if form_data['type'] == 'Watchlist':
                new_watchlist = Watchlist.objects.create(user=profile, currency=currency)
            elif form_data['type'] == 'Portfolio':
                new_watchlist = Portfolio.objects.create(user=profile, currency=currency)
            new_watchlist.save()

    elif request.method == 'POST' and 'source' in str(request.POST):
        print('set source')
        print(request.POST)
        source_form = SetSource(request.POST)
        if source_form.is_valid():
            form_data = source_form.cleaned_data
            exchange = Exchange.objects.get(id=form_data['source'])
            watch_coin = WatchlistCoins.objects.get(id=form_data['coin'])
            watch_coin.source = exchange
            print(f'source changed to {form_data["source"]}')
        else:
            print(f'errors: {source_form.errors}')

    else:
        context['add_form'] = AddToPortfolio()
        context['change_form'] = ChangeCurrency()

        context['currency'] = portfolio.currency
        context['portfolio'] = portfolio
        context['coins'] = coins
        context['coins_in_pf'] = coins_in_pf
        try:
            context['value'] = get_portfolio_value(coins_in_pf, portfolio.currency)
        except Exception as e:
            context['value'] = 0

    return render(request, 'watchlist/watchlist.html', context)

