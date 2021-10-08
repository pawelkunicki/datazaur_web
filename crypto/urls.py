from django.urls import path

from . import views

app_name = 'crypto'
urlpatterns = [
    path('', views.crypto, name='crypto'),
    path('exchanges/', views.exchanges, name='exchanges'),
    path('dominance/', views.dominance, name='dominance'),
    ]
