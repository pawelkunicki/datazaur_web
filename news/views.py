from django.shortcuts import render
from django.conf import settings
import requests
import pandas as pd
import os
# Create your views here.



def news(request):
    api_key = os.environ.get('CRYPTOCOMPARE_API_KEY')
    url = f'https://min-api.cryptocompare.com/data/v2/news/?lang=EN&api_key={api_key}'

    df = pd.json_normalize(requests.get(url).json()['Data'])[['published_on', 'title', 'url', 'source', 'body',
                                                              'categories']]
    df.loc[:, 'body'] = df.loc[:, 'body'].apply(lambda x: x[:320] + '...')

    df['title'] = df.apply(lambda x: f"""<a href="{x['url']}">{x['title']}</a>""", axis=1)
    df['published_on'] = df['published_on'].apply(lambda x: pd.to_datetime(x*10**9), True)
    df.drop('url', axis=1, inplace=True)
    df.columns = ['Date', 'Title', 'Source', 'Text', 'Categories']
    context = {'table': df.to_html(justify='center', escape=False)}
    return render(request, 'news/news.html', context)




def calendar(request):
    context = {}

    return render(request, 'news/calendar.html')