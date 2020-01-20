from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .models import *
from .forms import RegisterForm, LoginForm,  TraderForm, EditProfileForm, PasswordChange, UploadedFileForm, DepositForm
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from django.conf import settings
from django.urls import reverse
import datetime
import requests
# from django.core.context_processors import csrf
# Create your views here.

import stripe

stripe.api_key = settings.STRIPE_SECRET



def index(request):
    # if request.user.is_authenticated:
    #     return redirect('/trade/tradenow')

    context = {
        "title": "TradingOption247",
        "address": "Miami Florida",
        "phone_no": "+123456789",
        "country": "United States",
        "email": "support@tradingoption247.com",
        "whatsapp": "+123456789",
    }
    return render(request, "tradeoption/index.html", context)

@login_required
def accounts(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        profile_form = TraderForm(request.POST,instance=request.user.trader)
        if user_form.is_valid() and profile_form.is_valid():

            user_form = user_form.save()
            profile_form = profile_form.save(False)
            profile_form.user = user_form
            profile_form.save()
            return redirect('/accounts')
    else:
        user_form = EditProfileForm(instance=request.user)
        profile_form = TraderForm(instance=request.user.trader)
  

    return render(request, "tradeoption/account-details.html", {'r_form':user_form, 't_form':profile_form})

@login_required
def change_password(request):
    if request.method == "POST":
        password_change_form = PasswordChange(request.user, request.POST)
        if password_change_form.is_valid:
            pass
    else:
        password_change_form = PasswordChange(user=request.user)
    return render(request, "tradeoption/change-password.html", {'form':password_change_form})

@login_required
def account_summary(request):
    
    return render(request, "tradeoption/account-summary.html")

@login_required
def deposit(request):
    accounttypes = AccountType.objects.all()
    # curreny 
    ACCOUNT = {
        1 : 'Basic',
        2 : 'Premium',
        3 : 'Gold',
        4 : 'Vip',
        5 : 'Corp'
    }
    args = {}
    if request.method == "POST":
        amount = int(request.POST.get("amount").strip(" "))
        print("------------------------------------")
        print(request.POST.get("acc_type").strip(' '), type(request.POST.get("acc_type").strip(' ')))
        acc_type = float(request.POST.get("acc_type").strip(' '))
        if(amount < AccountType.objects.filter(a_type=acc_type)[0].price):

            args['accounttypes'] = accounttypes
            args["accounts"] = ACCOUNT
            args['publishable'] = settings.STRIPE_PUBLISHABLE
            args["error"] = f"* Minumum amount required is {AccountType.objects.filter(a_type=acc_type)[0].price}"
            return render(request, "tradeoption/deposit.html", args)
        else:
            try:
                customer = stripe.Customer.create(
                    email = request.POST.get("stripeEmail"),
                    source = request.POST.get("stripeToken")

                )

                charge = stripe.Charge.create(
                    customer = customer.id,
                    amount=amount*100,
                    currency=request.user.trader.preferred_currency.code.lower(),
                    description= f'{ACCOUNT[acc_type]} investment plan'
                )
                print("=============================")
                if (charge.outcome.seller_message == "Payment complete." and charge.outcome.type == "authorized", charge.refunded == False):
                    transaction = AccountTransaction.objects.get(user=request.user)
                    
                    transaction.description=f'{ACCOUNT[acc_type]} investment plan'
                       
                    transaction.save()

                    AccountTransaction.deposit(AccountTransaction.objects.get(user=request.user).id, amount)
                    return redirect('/trade')


                # session = stripe.checkout.Session.create(
                #     payment_intent_data={ 
                #         'setup_future_usage': 'off_session',
                #         'capture_method': 'manual',
                #     },
                #     # customer = request.user.trader.id,
                #     payment_method_types=['card'],
                #     line_items=[{
                #         'name': 'noth',#ACCOUNT[acc_type],
                #         'description': "nothing",#f'{ACCOUNT[acc_type]} investment plan',
                #         'amount': 50000,#amount*100,
                #         'currency': "usd",#request.user.trader.preferred_currency.code.lower(),
                #         'quantity': 1,
                #     }],
                #     success_url= 'https://example.com/success',
                #     cancel_url= 'https://example.com/cancel',
                #     )
                # print("=============================")
                # print(session)
                # args['session_id'] = session.id
            except stripe.error.CardError as e:
                print('e')
        # if form.is_valid():
            
                # customer = stripe.Charge.create(
                #     amount = form.cleaned_data['amount'], 
                #     currency = 'USD',
                #     description = form.cleaned_data['email'],
                # )
                # form.save()
                # print('\n')
                # print(customer)

                # redirect('/trade')
            
    
    
                # form.add_error('The card has been declined')
    # else:
    #     form = DepositForm()
    
    
    args['accounttypes'] = accounttypes
    args["accounts"] = ACCOUNT
    # args.update(csrf(request))
    
    # args['form'] = form
    args['publishable'] = settings.STRIPE_PUBLISHABLE
    
    return render(request, "tradeoption/deposit.html", args)

@login_required
def history(request):

    return render(request, "tradeoption/history.html")

@login_required
def message(request):

    return render(request, "tradeoption/message.html")

@login_required
def trade(request):
    if request.method == 'POST':
        print("--------------hello-----------------")
        print(request.user.uploadedfile.status)
        print("--------------hello-----------------")
    if request.user.uploadedfile.status:
        msg = request.user.uploadedfile.status
        # if int(msg) == 2 or int(msg) == 3:
        #     return render(request, "tradeoption/trade.html", {'msg':msg, "redirect":"tradeoption/tradenow.html"}) 

    return render(request, "tradeoption/trade.html", {'msg':msg,"redirect":"" })

@login_required
def trade_now(request):
    msg = request.user.uploadedfile.status
    print(msg, '------------------------------------------------------------------------------------------')
    if int(msg) <= 1:
        if request.method == 'POST' or request.method == "GET":
            return redirect('/trade')

    else:
        return render(request, "tradeoption/tradenow.html")
def csv_temp(request):
    # from alpha_vantage.foreignexchange import ForeignExchange
    from alpha_vantage.timeseries import TimeSeries
    from alpha_vantage.techindicators import TechIndicators
    key = 'Y60HOLBBWTXXE4V4'

    # url = 'https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=5min&apikey=Y60HOLBBWTXXE4V4'
    # res = requests.get(url)

    ts = TimeSeries(key, output_format="json")#ForeignExchange(key, output_format="json")
    ti = TechIndicators(key) 
    aapl_data, aapl_meta_data = ts.get_intraday(symbol='AAPL', interval='1min')
    # print(aapl_data)
    return JsonResponse(aapl_data)
@login_required
def verify(request):
    if request.method == "POST":
        form = UploadedFileForm(request.POST, request.FILES, instance=request.user.uploadedfile)
        if form.is_valid():
            form.save(commit=False)
            # print("\n \n")
            # print(f'{request.user.uploadedfile.status}')
            # print("\n \n")
            form.user = request.user
            # print("\n \n")
            # print(f'{form.user.uploadedfile.status}')
            # print("\n \n")
            form.user.uploadedfile.status = 2
            form.save()
            # print("-------------hello------------")
            return redirect("/trade")
    else:
        form = UploadedFileForm()
    return render(request, "tradeoption/verify.html", {"form":form})

@login_required
def withdrawal_history(request):

    return render(request, "tradeoption/whistory.html")

@login_required
def withdraw(request):

    return render(request, "tradeoption/withdraw.html")


def accounttype(request):
    return render(request, "tradeoption/accounttype.html")

def login_view(request):
    msg = None
    if request.method == 'POST' and request.POST.get('log'):
        form = LoginForm(data=request.POST)
        if form.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            print(redirect(request.GET['next']))
            print('Hello')
            print(redirect(request.GET['next']))
            print(redirect(request.GET['next']))
            if request.GET['next'] and user:
                login(request,user)
                print(redirect(request.GET['next']))
            elif user:
                login(request,user) 
            else :
                msg = 'Invalid credentials'
    
    else:
        form = LoginForm()

    print(redirect(request.GET.args))
    return render(request, "tradeoption/login.html", {'form_login':form, 'error_msg':msg})

@transaction.atomic
def register(request):
    if request.user.is_authenticated:
        return redirect('/trade/tradenow')
    if request.method == 'POST' and request.POST.get('reg'):
        user_form = RegisterForm(request.POST)
        profile_form = TraderForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            user.set_password(password)
            user.trader = profile_form.save(commit=False)
            account = stripe.Account.create(
                country= Country.objects.get(pk=request.POST.get('country_id')).code,
                type='custom',
                default_currency= profile_form.cleaned_data['preferred_currency'],
                email= user_form.cleaned_data['email'],
                requested_capabilities=['card_payments', 'transfers'],
            )

            transaction = AccountTransaction(
                        user=user,
                        currency=profile_form.cleaned_data['preferred_currency'],
                        stripe_id=account.id,
                        )
            transaction.save()
            
            user.save()
            for field in profile_form.changed_data:
                setattr(user.trader, field, profile_form.cleaned_data[field])
            user.trader.save()
        
            

            user = authenticate(username=username, password=password)
            
            
            # print("======================== user =====================")
            if user is not None:
                if user.is_active:
                    print("======================== user =====================")
                    print(user, user.is_active)
                    print("======================== user =====================")
                    login(request, user)
                    return redirect('/trade') 
    else:
        user_form = RegisterForm()
        profile_form = TraderForm()

    return render(request, "tradeoption/register.html", {'r_form': user_form, 't_form':profile_form})

# def trade(request):
#     return render(request, "tradeoption/trade.html")

def about(request):
    return render(request, "tradeoption/about.html")

def contact(request):
    return render(request, "tradeoption/index.html/#contact")

def binary_options(request):
    return render(request, "tradeoption/binaryoptions.html")

def ifollow(request):
    return render(request, "tradeoption/ifollow.html")

def ladder(request):
    return render(request, "tradeoption/ladder.html")

def onetouch(request):
    return render(request, "tradeoption/onetouch.html")

def about(request):
    return render(request, "tradeoption/about.html")

def termsOfUse(request):
    return render(request, "tradeoption/terms_of_use.html")

def privacy(request):
    return render(request, "tradeoption/privacy.html")

def disclaimer(request):
    return render(request, "tradeoption/disclaimer.html")

def security(request):
    return render(request, "tradeoption/security.html")

def forgot(request):
    return render(request, "tradeoption/forgot.html")

# class UserFormView(View):
#     form_class = UserForm
#     template_name = 'tradeoption/login.html'

#     def get(self, request):
#         form = self.form_class(None) 
#         return render(requst, self.template_name, {'form': form})

#     def post(self, request):
#         form = self.form_class(request.POST)

#         if form.is_valid():
#             user = form.save(commit=False)
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user.set_password(password)
#             login(request, user)
#             user.save()

#             # returns User objects if credentials are correct 
#             user = authenticate(username=username, password=password)

#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('')
#         return render(requst, self.template_name, {'form': form})