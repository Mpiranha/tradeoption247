from django.db import models
from .currencies import CurrencyCurrencies
from .currency import Currency
from datetime import datetime

class CurrencyItems(Currency):
    pass

class Item(models.Model):
    code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    currency_id = models.ForeignKey(CurrencyCurrencies, on_delete=models.CASCADE)
    details = models.CharField(max_length=1024)

class Price(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    currency_id = models.ForeignKey(CurrencyCurrencies, on_delete=models.CASCADE)
    buy = models.FloatField(default=0)
    sell = models.FloatField(default=0)
    timestamp = models.DateTimeField(default=datetime.now)

class Report:
    trading_date = models.DateTimeField(default=datetime.now, null=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    currency_id = models.ForeignKey(CurrencyItems, on_delete=models.CASCADE)
    first_price = models.FloatField(default=0, null=True)
    last_price = models.FloatField(default=0, null=True)
    min_price = models.FloatField(default=0, null=True)
    max_price = models.FloatField(default=0, null=True)
    avg_price = models.FloatField(default=0, null=True)
    total_price = models.FloatField(default=0, null=True)
    total_amount = models.FloatField(default=0, null=True)
    quantity = models.FloatField(default=0, null=True)



