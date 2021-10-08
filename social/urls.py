

from django.urls import path

from . import views

app_name = 'messenger'
urlpatterns = [
    path('messenger', views.messenger, name='messenger'),
    path('top_traders', views.top_traders, name='top_traders'),
    path('top_strategies', views.top_strategies, name='top_strategies'),
    ]



