from rest.settings import *
import os

DATABASE_ROUTERS = ["api.tests.mongo_tests.mongo_db_router.DB_Router"]
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'twitter',
        'HOST': os.environ['MONGO_HOST'],
        'PORT': int(os.environ['MONGO_PORT']),
        'USER': 'admin',
        'PASSWORD': 'admin',
    },

}