from django.shortcuts import render
from django.conf import settings
import requests
import pandas as pd
import investpy
import os
from .forms import AddWebsite
from .models import Website
from utils.other_data import *
from utils.news_scrapper import *
from website.models import UserProfile
# Create your views here.



def news(request):
    context = {}
    crypto_news = cryptocomp_news()
    context['crypto_news'] = crypto_news.to_html(justify='center', escape=False)

    scapped_news = {}
    news = scrap_news()
    for k,v in news.items():
        scapped_news[k] = pd.DataFrame(v).transpose().to_html(escape=False, justify='center')
    context['scrapped_news'] = scapped_news




    return render(request, 'news/news.html', context)

def websites(request):
    context = {}
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        websites = Website.objects.filter(user=profile)
        context['websites'] = websites
        context['add_form'] = AddWebsite()

        if request.method == 'POST':
            add_form = AddWebsite(request.POST)
            if add_form.is_valid():
                form_data = add_form.cleaned_data
                url = form_data['url']
                selector = form_data['selector']
                title = url.split('//')[1].split('.')[0]
                profile = UserProfile.objects.get(user=request.user)
                website = Website.objects.create(user=profile, title=title, url=url, selector=selector)
                website.save()


    return render(request, 'news/websites.html', context)


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



