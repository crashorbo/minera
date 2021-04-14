from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ADMINS = (
    ('Alexander Calani', 'alexander.calani.apaza@gmail.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'emcoisa',
        'USER': 'alexander',
        'PASSWORD': 'add150806',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
