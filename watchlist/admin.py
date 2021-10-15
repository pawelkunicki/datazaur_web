from django.contrib import admin
from .models import WatchlistCoins, Watchlist, Portfolio, Amounts
# Register your models here.

admin.site.register(Watchlist)
admin.site.register(WatchlistCoins)
admin.site.register(Portfolio)
admin.site.register(Amounts)



