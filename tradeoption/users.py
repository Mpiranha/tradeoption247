from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from .currencies import Country
from .currency import Currency
from .items import Item
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from .validators import check_positive
from django.db.models import Max
from django.db import transaction
from django.core.exceptions import FieldError
class CurrencyTraders(Currency):
    pass

class Trader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="trader")
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, related_name="country")
    # state = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    phone = models.IntegerField(default=0)
    confirmation_code = models.CharField(max_length=128, null=True)
    date_created = models.DateTimeField(default=datetime.now)
    date_confrirmed = models.DateTimeField(default=datetime.now, blank=True)
    preferred_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, related_name="currency")


class AccountTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction')
    date = models.DateTimeField(default=datetime.now)
    description = models.CharField(max_length=1028, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    stripe_id = models.CharField(max_length=128, null=True)
    balance = models.IntegerField(default=0,)

    @classmethod
    def deposit(cls, id, amount):
        with transaction.atomic():
            account = (
                cls.objects
                    .select_for_update()
                        .get(id=id)
                )
      
            print(account, 'account')
            account.balance += amount
            account.save()
        return account
    @classmethod
    def withdraw(cls, id, amount):
        with transaction.atomic():
            account = (
                cls.objects
                    .select_for_update()
                            .get(id=id)
                )
      
        if account.balance < amount:
           raise FieldError
        account.balance -= amount
        account.save()
  
        return account


class AccountBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balance')
    transaction = models.ForeignKey(AccountTransaction, on_delete=models.CASCADE, null=True )
    balance = models.FloatField(default=0, validators=[check_positive]) 
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)  

class AccountType(models.Model):
    BASIC = 1
    PREMIUM = 2
    GOLD = 3
    VIP = 4
    CORP = 5
    ACCOUNT = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
        (GOLD, 'Gold'),
        (VIP, 'Vip'),
        (CORP, 'Corp')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account_type', null=True)
    a_type= models.IntegerField(choices = ACCOUNT, default=1)
    price = models.FloatField(default=0)
    bonus = models.FloatField(default=0)
    level = models.IntegerField(default=1)
    risky = models.BooleanField(default=True)
    training  = models.BooleanField(default=False)
    trading_signal = models.BooleanField(default=False)



class UploadedFiles(models.Model):
    STATE_UPLOADED = 1
    STATE_VERIFYIING = 2
    STATE_VERIFIED = 3
    STATE = (
        (STATE_UPLOADED, "Uploaded"),
        (STATE_VERIFYIING, 'Verifying'),
        (STATE_VERIFIED, 'Verified')
    )

    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='uploadedfile')
    title = models.CharField(max_length=128, default='Document 1', null=True)
    status = models.SmallIntegerField(choices=STATE, default=0, null=True)
    _file = models.ImageField(upload_to=f'upload/user_id/documents/%Y/%m/%d/', null=True)

    def __str__(self):
        return self.title
    
    def name(self):
        return os.path.basename(self._file.name)
    
    def save(self, *args, **kwargs):
        if not self.status:
            self.status = self.STATE_UPLOADED
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        os.remove(self._file.path)
        self._file.delete(False)
        super().delete(*args, **kwargs)

@receiver(post_save, sender=User)
def user_is_created(sender, instance, created, **kwargs):
    if created:
        Trader.objects.create(user=instance)
        # AccountTransaction.objects.create(user=instance)
        # AccountBalance.objects.create(user=instance)
        UploadedFiles.objects.create(user=instance)
    else:
        # instance.transaction.save()
        # instance.balance.save()
        instance.trader.save()
        instance.uploadedfile.save()
        

# @receiver(post_save, sender=User)
# @receiver(post_save, sender=AccountTransaction)
# def transaction_is_created(sender, instance, created, **kwargs):
#     # print("tranc ", instance.user, instance.user.transaction.all())
#     if created:
#         last_transaction = instance.user.transaction.all()[len(instance.user.transaction.all())-1]
#         if instance.user.balance.all():
#             balance = instance.user.balance.get(pk=instance.user.balance.all().aggregate(Max("id"))["id__max"]).balance + last_transaction.amount
#             AccountBalance.objects.create(user=instance.user, transaction = instance, balance=balance, currency= instance.currency)
#         # bal.balance = bal.balance + last_transaction.amount
             
#         # print(bal.balance)
#         else:
#            a = AccountBalance(user=instance.user, transaction=instance, balance=last_transaction)
#            a.save() 
        #
    #     AccountBalance.objects.create(trader=instance)
    #     UploadedFiles.objects.create(user=instance)
    # else:
    #     instance.trader.save()
    #     instance.uploadedfile.save()

# @receiver(post_save, sender=Currency)
# def currency_is_created(sender, instance, created, **kwargs):
#     if created:

class Offer(models.Model):
    trader_id = models.ForeignKey(Trader, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.FloatField(blank=True)
    buy = models.BooleanField(default=False)
    sell = models.BooleanField(default=False)
    price = models.FloatField(blank=True)
    timestamp = models.DateTimeField(default=datetime.now)
    is_active = models.BooleanField(default=False)


class Trade(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    seller_id = models.ForeignKey(Trader, on_delete=models.CASCADE, related_name='seller')
    buyer_id = models.ForeignKey(Trader, on_delete=models.CASCADE, related_name='buyer')
    quantity = models.FloatField(null=True)
    unit_price = models.FloatField(null=True)
    description = models.CharField(max_length=1024)
    offer_id = models.ForeignKey(Offer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now)

class CurrentInventory(models.Model):
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.FloatField(blank=True)


