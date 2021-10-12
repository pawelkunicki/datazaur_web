
from django.urls import path

from . import views

app_name = 'trade'
urlpatterns = [
    path('trade/', views.trade, name='trade'),
    path('cointegration/', views.cointegration, name='cointegration'),
    path('momentum/', views.momentum, name='momentum'),
    path('arbitrage/', views.arbitrage, name='arbitrage'),
    path('history/', views.history, name='history'),
    ]



