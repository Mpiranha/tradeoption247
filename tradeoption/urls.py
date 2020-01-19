from . import views
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth.urls import
from .forms import LoginForm, PasswordReset, PasswordResetConfirm, PasswordChange

urlpatterns = [
    path("", views.index, name = "index"),
    # path("payment-url/", views.buy_my_item, name='payment'),
    # path("paypal/", include("paypal.standard.ipn.urls")),
    path("trade/tradenow/data", views.csv_temp, name='csv'),
    path("trade/tradenow/", views.trade_now, name='tradenow'),
    path("accounts/", views.accounts, name = "account-details"),
    path("deposit/", views.deposit, name = "deposit"),
    path("history/", views.history, name = "history"),
    path("message/", views.message, name = "message"),
    path("trade/", views.trade, name = "trade"),
    path("account-summary/", views.account_summary, name = "account-summary"),
    path("change-password/", auth_views.PasswordChangeView.as_view(form_class = PasswordChange) , name = "change-password"), #
    path("password_change_done/", auth_views.PasswordChangeDoneView.as_view() , name = "password_change_done"),
    path("verify/", views.verify, name = "verify"),
    path("withdraw/", views.withdraw, name = "withdraw"),
    path("withdrawal-history/", views.withdrawal_history, name = "whistory"),
    path("index/", views.index, name = "index"),
    path("accounttype/", views.accounttype, name = "accounttype"),
    path("logout/", auth_views.LogoutView.as_view(next_page='index'), name = "logout"),
    path("login/", auth_views.LoginView.as_view(authentication_form=LoginForm, redirect_authenticated_user=True), name = "login"),
    path("accounts/login/", auth_views.LoginView.as_view(authentication_form=LoginForm, redirect_authenticated_user=True), name = "login"),
    path("register/", views.register, name = "register"),
    path("trade/", views.trade, name = "trade"),
    path("about/", views.about, name = "about"),
    path("contact/", views.contact, name = "contact"),
    path("ladder/", views.ladder, name = "ladder"),
    path("binaryoptions/", views.binary_options, name = "binaryoptions"),
    path("ifollow/", views.ifollow, name = "ifollow"),
    path("onetouch/", views.onetouch, name = "onetouch"),
    path("about/", views.about, name = "about"),
    path("termsOfUse/", views.termsOfUse, name = "termsOfUse"),
    path("disclaimer/", views.disclaimer, name = "disclaimer"),
    path("security/", views.security, name = "security"),
    path("privacy/", views.privacy, name = "privacy"),
    # path("forgot/", views.forgot, name = "forgot"),
    path("password_reset/", auth_views.PasswordResetView.as_view(form_class = PasswordReset), name = "forgot"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name = "password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(form_class = PasswordResetConfirm), name ="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name = "password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)