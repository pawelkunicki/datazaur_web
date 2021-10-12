import pandas as pd
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .forms import AddToPortfolio, ChangeCurrency
from .models import Watchlist, WatchlistCoins, Portfolio, Amounts
from markets.models import Currency
from crypto.models import Cryptocurrency
from utils.portfolio_value import get_portfolio_value
from website.models import UserProfile


@login_required
def watchlist(request):
    context = {}
    profile = UserProfile.objects.get(user=request.user)
    portfolio = Portfolio.objects.get(user=profile)
    coins = Cryptocurrency.objects.all()
    coins_in_pf = Amounts.objects.filter(portfolio=portfolio)

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
        chg_form = ChangeCurrency(request.POST)
        if chg_form.is_valid():
            data = chg_form.cleaned_data
            new_currency = Currency.objects.get(symbol=data['currency'])
            if portfolio.currency == new_currency:
                pass
            else:
                portfolio.currency = new_currency
                portfolio.save()
        else:
            print(f'errors: {chg_form.errors}')
        return HttpResponseRedirect(reverse('watchlist:watchlist', args=()))


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

