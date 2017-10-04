# -*- coding: utf-8 -*-
"""
Minimal dummy settings file
"""
import os


BASE_DIR = os.getcwd()
DEBUG = True
SECRET_KEY = 'thisisnotsecure'

INSTALLED_APPS = [
    'currencies',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SHOP_CURRENCIES = ('GBP',)
SHOP_DEFAULT_CURRENCY = 'GBP'
