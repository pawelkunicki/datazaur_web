from django.contrib import admin
from .models import Cryptocurrency, Exchange
# Register your models here.

admin.site.register(Cryptocurrency)
admin.site.register(Exchange)

