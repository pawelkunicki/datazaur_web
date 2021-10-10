import pandas as pd
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .forms import AddToPortfolio, ChangeCurrency


from utils.portfolio_value import get_portfolio_value
from website.models import UserProfile
# Create your views here.


def markets(request):
    context={}


    return render(request, 'markets/markets.html', context)


def crypto(request):
    context = {}

    return render(request, 'markets/crypto.html', context)

def forex(request):
    context = {}

    return render(request, 'markets/forex.html', context)

def indices(request):
    context = {}

    return render(request, 'markets/indices.html', context)

def stocks(request):
    context = {}

    return render(request, 'markets/stocks.html', context)

def bonds(request):
    context = {}

    return render(request, 'markets/bonds.html', context)

def commodities(request):
    context = {}

    return render(request, 'markets/commodities.html', context)


