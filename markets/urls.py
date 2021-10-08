
from django.urls import path

from . import views

app_name = 'markets'
urlpatterns = [
    path('', views.crypto, name='markets'),
    path('indices/', views.indices, name='indices'),
    path('forex/', views.forex, name='forex'),
    path('bonds/', views.bonds, name='bonds'),
    path('stocks/', views.stocks, name='stocks'),
    path('commodities/', views.commodities, name='commodities'),
    ]
