from django.urls import path

from . import views

app_name = 'watchlist'
urlpatterns = [
    path('', views.watchlist, name='watchlist'),
    ]
