from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ADMINS = (
    ('Alexander Calani', 'alexander.calani.apaza@gmail.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'minera_env',
        'USER': 'alexander',
        'PASSWORD': 'add150806',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
