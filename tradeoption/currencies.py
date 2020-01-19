from django.db import models
from datetime import datetime
from .currency import Currency

class CurrencyCurrencies(Currency):
    pass

class Country(models.Model):
    name = models.CharField(max_length=128, unique = True)

    def __str__(self):
        return self.name


class CurrencyUsed(models.Model):
    # maps country to currency and date from where the currency was used
    # if the date to is None the the currency is currently in use.
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    currency_id = models.ForeignKey(CurrencyCurrencies, on_delete=models.CASCADE)
    date_from = models.DateTimeField(default=datetime.now)
    date_to = models.DateTimeField(default=datetime.now, null=True)


class CurrencyRate(models.Model):
    currency_id = models.ForeignKey(CurrencyCurrencies, on_delete=models.CASCADE, related_name='intrested_currency')
    base_currency_id = models.ForeignKey(CurrencyCurrencies, on_delete=models.CASCADE,related_name='base_currency')
    rate = models.FloatField(default=0)
    timestamp = models.DateTimeField(default=datetime.now)
    
