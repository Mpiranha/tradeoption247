"""
Django settings for tradingoption247 project.

G0enerated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import django_heroku
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u7p5_v3m6ylsyyf(@g$@1n2)cv(cwkdwjo^--k)3tt4=-o44^0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'tradeoption.apps.TradeoptionConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'paypal.standard',
    # 'paypal.pro',
    # 'encrypted_model_fields',
]
# AUTH_USER_MODEL = 'tradeoption.Users'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tradingoption247.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tradingoption247.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# ------------MEDIA--------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'files')

LOGIN_REDIRECT_URL = '/trade'
# LOGOUT_REDIRECT_URL = '/index'

# -------------RECOVER PASSWORD EXPIREMENT SETTINGS ------------------
PASSWORD_RESET_TIMEOUT_DAYS = 1
 
 # ----------- SESSION SETTINGS ----------------------
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# -------------EMAIL SERVER SETTIINGS -----------------
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')

# --------------PAYPAL's INTEGRATION -----------------------------
PAYPAL_TEST = True
PAYPAL_RECIEVER_EMAIL = "sb-rmyhm630163@business.example.com"
PAYPAL_CLIENT_ID = "AXkMr5KTKNGhEiR5GiQMzhHJnjVk5Ac08rYzb2nOExRO6flZ0f6kUyZr5xfNRu3sWMU7kwHnh3TWjjCz"
PAYPAL_CLIENT_SECRET = "EDnYazE53-V01aFp3mNB4DBaBzsHXG2KakEn3oYg0MUdPYg8tc7t0qplrBxRrWggpvB_1VFmbCH7PYXS"

# -------------STRIPE INTEGRATION ------------------------------
STRIPE_PUBLISHABLE = 'pk_test_TPmPRLgc3LUTGMMBCwWVQLOG00b5fFjOx5'
STRIPE_SECRET = 'sk_test_5oqaXgp6lM2uVPLkmjlOD1fm00T5hykP5W'

# Activate Django-Heroku.
django_heroku.settings(locals())
