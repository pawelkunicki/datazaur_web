from bs4 import BeautifulSoup
import requests
import yaml
import os
import sys

filename = 'scrapper_selectors.yaml'


def load_websites():
    try:
        with open(filename, 'r') as file:
            return yaml.safe_load(file)
    except Exception:
        return None


def scrap_news():
    result = {}
    for website, selectors in load_websites().items():
        result[website] = []
        req = requests.get(website).text
        soup = BeautifulSoup(req, features='lxml')
        for selector in selectors:
            articles = soup.select(selector)
            #result[website].append([[article.a.text, article.a.get('href')] for article in articles])
            result[website].append(f'<a href="{article.a.get("href")}"> {article.a.text} </a>' for article in articles)

    return result


def add_website(url, selectors):
    if url in load_websites().keys():
        return 'Site already saved.'
    else:
        with open(filename, 'a') as file:
            yaml.dump({url: selectors}, file)
        print('added')







