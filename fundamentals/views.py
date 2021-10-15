import pandas as pd

from django.shortcuts import render
from utils.fundamentals import FundamentalData
from .forms import FindTicker
# Create your views here.


def fundamentals(request):
    context = {'search_form': FindTicker()}

    if request.method == 'GET' and 'ticker' in str(request.GET):
        print(request.GET)
        find_form = FindTicker(request.GET)
        if find_form.is_valid():
            form_data = find_form.cleaned_data
            print(form_data)
            ticker = form_data['ticker']
            context['ticker'] = ticker
            data = FundamentalData(ticker)
            context.update(data.get_fundamentals())
            print(context)
            context['price_history'] = data.get_price_history()
        else:
            print(find_form.errors)

        return render(request, 'fundamentals/fundamentals.html', context)

    else:
        return render(request, 'fundamentals/ticker_not_found.html', context)




