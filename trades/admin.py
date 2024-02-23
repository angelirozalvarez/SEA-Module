from django.contrib import admin

from .models import Trade, Trader, Bank

admin.site.register(Trade)
admin.site.register(Trader)
admin.site.register(Bank)
