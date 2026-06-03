import os
from pathlib import Path

# Glowna sciezka projektu
BASE_DIR = Path(__file__).resolve().parent

# Klucz bezpieczenstwa aplikacji
SECRET_KEY = 'django-insecure-test-key-zmien-w-produkcji'

# Tryb debugowania deweloperskiego
DEBUG = True

# Dozwolone domeny i hosty
ALLOWED_HOSTS = ['*']

# Lista aktywnych aplikacji systemu
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',  
    'django.contrib.messages',  
    'core',
]

# Procesy przetwarzajace zadania HTTP
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',  
]

# Glowny plik mapowania adresow URL
ROOT_URLCONF = 'urls'

# Konfiguracja silnika szablonow HTML
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

# Interfejs sieciowy serwera aplikacji
WSGI_APPLICATION = 'wsgi.application'

# Ustawienia polaczenia z baza danych
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Domyslny typ klucza glownego ID
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Strefa czasowa i tlumaczenia
USE_TZ = True
USE_I18N = True

# Adres URL dla plikow statycznych
STATIC_URL = 'static/'

# Folder z plikami CSS i obrazkami
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]