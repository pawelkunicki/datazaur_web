from django.urls import path

from . import views

app_name = 'macro'
urlpatterns = [
    path('', views.macro, name='macro'),
    path('calendar/', views.calendar, name='calendar'),
    ]
