from django.shortcuts import render
from django.conf import settings
import requests
import pandas as pd
import investpy
import os
from utils.other_data import *
# Create your views here.



def news(request):
    news = cryptocomp_news()
    context = {'news': news.to_html(justify='center', escape=False)}
    return render(request, 'news/news.html', context)

def crypto(request):
    news = cryptocomp_news()
    context = {'news': news.to_html(justify='center', escape=False)}
    return render(request, 'news/crypto.html', context)


def events(request):
    context = {}

    context['events'] = gecko_events()

    return render(request, 'news/events.html', context)


def calendar(request):
    context = {}

    context['calendar'] = investpy.economic_calendar().to_html(escape=False, justify='center')

    return render(request, 'news/calendar.html', context)



