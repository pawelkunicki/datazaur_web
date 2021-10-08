import datetime

from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import httpagentparser
from .models import UserProfile
from .forms import SelectCurrency
from portfolio.models import Portfolio
from watchlist.models import Watchlist
from forex.models import Currency
from utils.setup_db import setup_db, check_watchlists_and_portfolios
# Create your views here.


def home(request):
    context = {}
    if request.user.is_authenticated:
        print('authed')
        context['user'] = request.user
        context['currency_form'] = SelectCurrency()
        profile = UserProfile.objects.get(user=request.user)


    if request.method == 'POST' and 'currency' in str(request.POST):
        print(request.POST)

        currency_form = SelectCurrency(request.POST)
        if currency_form.is_valid():
            data = currency_form.cleaned_data
            user = request.user
            user.currency = Currency.objects.get(id=data['currency'])
            user.save()
            print(user.currency.name)


        else:
            print(f'errors: {currency_form.errors}')

    return render(request, 'website/home.html', context)



@login_required
def account(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    watchlist = profile.watchlist
    portfolio = profile.portfolio
    currency = profile.currency
    context = {'user': user, 'watchlist': watchlist, 'portfolio': portfolio}
    return render(request, 'website/account.html', context)


def log_in(request):
    if request.method == 'POST' and 'password' in request.POST:
        print(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        print(user)
        if user is not None:
            request.session.set_expiry(86400)
            login(request, user)
            context = {'user': user}
            return render(request, 'website/home.html', context)
        else:
            context = {'form': AuthenticationForm}
            return render(request, 'website/login_failed.html', context)
    else:
        return render(request, 'website/login.html', {'form': AuthenticationForm})


def signup(request):
    context = {'form': UserCreationForm}
    context['currencies'] = Currency.objects.all()
    currency = Currency.objects.get(symbol=settings.DEFAULT_CURRENCY)
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_data = user_form.cleaned_data
            user = User.objects.create_user(username=user_data['username'], password=user_data['password1'])
            user.save()
            profile = UserProfile.objects.create(user=user, currency=currency)

            request.session.set_expiry(86400)
            login(request, user)
            users_watchlist = Watchlist.objects.create(user=profile)
            users_watchlist.save()
            users_portfolio = Portfolio.objects.create(user=profile)
            users_portfolio.save()
            profile.save()

            context['user'] = user
            return render(request, 'website/home.html', context)
        else:
            print(user_form.errors)
            context['errors'] = dict(user_form.errors)
            print(context['errors'])
            return render(request, 'website/signup_failed.html', context)

    else:
        return render(request, 'website/signup.html', context)


def log_out(request):
    logout(request)
    return render(request, 'website/logout.html')



def downloads(request):
    if request.method == 'POST':
        pass    # Datazaur desktop download will go here

    else:
        agent = request.META['HTTP_USER_AGENT']
        os = httpagentparser.detect(agent)['os']
        print(os)

        context = {'os': os}

        return render(request, 'website/downloads.html', context)

