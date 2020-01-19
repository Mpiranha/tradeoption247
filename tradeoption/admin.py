from django.contrib import admin
from .models import Currency, Trader, Country, UploadedFiles, AccountType
# Register your models here.

admin.site.register(Currency)
admin.site.register(Trader)
admin.site.register(Country)
admin.site.register(UploadedFiles)
admin.site.register(AccountType)


