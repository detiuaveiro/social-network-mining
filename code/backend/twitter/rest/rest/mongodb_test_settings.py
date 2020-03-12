from rest.settings import *


DATABASE_ROUTERS = ["api.tests.mongo_tests.mongo_db_router.DB_Router"]
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
