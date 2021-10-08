
from django.urls import path

from . import views

app_name = 'trading'
urlpatterns = [
    path('trade/', views.trade, name='trade'),
    path('algorithms/', views.algorithms, name='algorithms'),
    path('arbitrage/', views.arbitrage, name='arbitrage'),
    path('history/', views.history, name='history'),
    ]



