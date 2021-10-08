import pandas as pd

from django.shortcuts import render
from utils.fundamentals import FundamentalData
from .forms import FindTicker
# Create your views here.


def fundamentals(request):
    context = {'search_form': FindTicker()}

    if request.method == 'GET' and 'ticker' in str(request.GET):
        ticker = request.GET['ticker']
        context['ticker'] = ticker
        data = FundamentalData(ticker)
        context.update(data.get_fundamentals())
        context['price_history'] = data.get_price_history()
        return render(request, 'fundamentals/fundamentals.html', context)

    else:
        return render(request, 'fundamentals/ticker_not_found.html', context)




