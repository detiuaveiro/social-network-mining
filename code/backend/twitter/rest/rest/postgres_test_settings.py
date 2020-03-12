from rest.settings import *

DATABASE_ROUTERS = ["api.tests.postgresql_tests.postgres_db_router.DB_Router"]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'twitter_postgres',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
