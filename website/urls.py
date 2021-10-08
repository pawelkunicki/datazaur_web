from django.urls import path

from . import views

app_name = 'website'
urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.log_in, name='login'),
    path('signup', views.signup, name='signup'),
    path('log_out', views.log_out, name='log_out'),
    path('account', views.account, name='account'),
    path('downloads', views.downloads, name='downloads'),
    ]



