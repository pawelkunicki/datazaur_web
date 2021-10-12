from django.urls import path

from . import views

app_name = 'crypto'
urlpatterns = [
    path('', views.crypto, name='crypto'),
    path('exchanges/', views.exchanges, name='exchanges'),
    path('dominance/', views.dominance, name='dominance'),
    path('global_metrics/', views.global_metrics, name='global_metrics'),
    path('trends/', views.trends, name='trends'),
    path('defi/', views.defi, name='defi'),
    path('nft/', views.nft, name='nft'),
    path('icos/', views.icos, name='icos'),
    path('wallets/', views.wallets, name='wallets'),
    path('games/', views.games, name='games'),
    ]
