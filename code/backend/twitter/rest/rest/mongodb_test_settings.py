from rest.settings import  *

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'twitter',
        'HOST': '127.0.0.1',
        'PORT': 27017,
        'USER': 'admin',
        'PASSWORD': 'admin',
    },

}