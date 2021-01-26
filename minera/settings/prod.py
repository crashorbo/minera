from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ADMINS = (
    ('Alexander Calani', 'alexander.calani.apaza@gmail.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd13vn99tm5dsb2',
        'USER': 'qrabwjwrgvikmm',
        'PASSWORD': 'bc23325b1f12992df718faf8ffb9d49a2fefb6191d6b183cae58052484891a7d',
        'HOST': 'ec2-54-211-55-24.compute-1.amazonaws.com',
        'POST': 5432,
    }
}
