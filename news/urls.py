from django.urls import path

from . import views

app_name = 'news'
urlpatterns = [
    path('', views.news, name='news'),
    path('crypto/', views.crypto, name='crypto'),
    path('events/', views.events, name='events'),
    path('calendar/', views.calendar, name='calendar'),
    ]
