from django.urls import path

from . import views

app_name = 'fundamentals'
urlpatterns = [
    path('', views.fundamentals, name='fundamentals'),
    ]