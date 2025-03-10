"""datazaur URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', include('website.urls'), name='website'),
    path('markets/', include('markets.urls'), name='markets'),
    path('trade/', include('trade.urls'), name='trade'),
    path('macro/', include('macro.urls'), name='macro'),
    path('fundamentals/', include('fundamentals.urls'), name='fundamentals'),
    path('crypto/', include('crypto.urls'), name='crypto'),
    path('watchlist/', include('watchlist.urls'), name='watchlist'),
    path('messenger/', include('messenger.urls'), name='messenger'),
    path('news/', include('news.urls'), name='news'),
    path('social/', include('social.urls'), name='social'),

]

