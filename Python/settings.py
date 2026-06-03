import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = 'django-insecure-test-key-zmien-w-produkcji'
DEBUG = True
ALLOWED_HOSTS = ['*']

# POPRAWIONE: Dodaliśmy na samą górę 'django.contrib.staticfiles'
INSTALLED_APPS = [
    'django.contrib.staticfiles',  # <- KLUCZOWA LINIA! Bez tego CSS nigdy nie ruszy
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',  
    'django.contrib.messages',  
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',  
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages', 
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

USE_TZ = True
USE_I18N = True

# ==========================================================================
# PLIKI STATYCZNE (CSS, OBRAZKI)
# ==========================================================================
STATIC_URL = 'static/'

# POPRAWIONE: Zamiast sztywnego dysku C:, używamy BASE_DIR. 
# Django samo znajdzie folder 'static' obok pliku manage.py
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]