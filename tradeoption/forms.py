from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, UserCreationForm, PasswordChangeForm
from django.forms.widgets import PasswordInput, TextInput
from django import forms
from django.contrib.auth.models import User
from .models import Currency, Trader, Country, UploadedFiles, AccountTransaction
from django.core.exceptions import NON_FIELD_ERRORS

class DepositForm(forms.ModelForm):
    
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    amount = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Amount'}))
    card_no = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number', 'min':'99999999999'}))
    cvv = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'cvv', 'min':'999'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Pin', 'min':'999', 'max':'9999'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Fullname on Card '}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip Code'}))
    stripe_id = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip Code', 'hidden':'true'}))
    edate = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'form-control', 'type':'date','id':'details'}))
   
    class Meta:
        model = AccountTransaction
        fields = ['email','amount', 'stripe_id']

    # def add_error(self, message):
    #     self._errors[NON_FIELD_ERRORS] = self.error_class([nessaage])
class RegisterForm(UserCreationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password confirmation'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Firstnane', 'Required':'false'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Lastname', 'Required':'false'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
   
    



    class Meta:
        model = User
        fields = ['username', 'password1' ,'password2','first_name','last_name','email' ]
        # widgets = {
        #     'username' : TextInput(attrs={'class':'form-control', 'placeholder':'Username'}),
        #     'password1' : PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}),
        #     'password2' : PasswordInput(attrs={'class':'form-control', 'placeholder':'Password Confirmation'}),
        #     'first_name' : TextInput(attrs={'class':'form-control', 'placeholder':'Firstname'}),
        #     'last_name' : TextInput(attrs={'class':'form-control', 'placeholder':'Lastname'}),
        #     'email' : TextInput(attrs={'class':'form-control', 'placeholder':'Email'})

        # }

class TraderForm(forms.ModelForm):

    country_id = forms.ModelChoiceField(queryset=Country.objects.all(), initial=0, widget=forms.Select(attrs={'class':'form-control','placeholder':'Country'}))
    # state = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}))
    # city = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'City'}))
    preferred_currency = forms.ModelChoiceField(queryset=Currency.objects.all(),  initial=0, widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Currency'}))
    phone = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone', 'Required':'false'}))
    
    class Meta:
        model = Trader
        fields = [ 'country_id', 'preferred_currency', 'phone' ]
 

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Firstnane'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Lastname'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email', 'readonly':'true'}))
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email' )


    
class LoginForm(AuthenticationForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))


class PasswordReset(PasswordResetForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))

class PasswordResetConfirm(SetPasswordForm):
    def __init__(self,user,*args, **kwargs):
        super().__init__(user,*args, **kwargs)
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password Confirmation'}))
    field_order = ['password1', 'password2']

class PasswordChange(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'New Password Confirmation'}))
    
class UploadedFileForm(forms.ModelForm):
    title = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Name of Document'}))
    class Meta:
        model = UploadedFiles
        fields = ['title','_file']