
from django.urls import path
from crypto.views import crypto
from . import views

app_name = 'markets'
urlpatterns = [
    path('', views.markets, name='all_markets'),
    path('crypto/', crypto, name='crypto'),
    path('indices/', views.indices, name='indices'),
    path('forex/', views.forex, name='forex'),
    path('forex_matrix/', views.forex_matrix, name='forex_matrix'),
    path('bonds/', views.bonds, name='bonds'),
    path('stocks/', views.stocks, name='stocks'),
    path('funds/', views.funds, name='funds'),
    path('etfs/', views.etfs, name='etfs'),
    path('commodities/', views.commodities, name='commodities'),
    path('trends/', views.trends, name='trends'),
    ]
