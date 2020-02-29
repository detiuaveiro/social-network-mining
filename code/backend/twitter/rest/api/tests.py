from django.test import TestCase

# Create your tests here.
from api.models import TestMongo, TestPostgres

mongo = TestMongo.objects.create(x=2, y=2)
postgres = TestPostgres.objects.create(x=2, y=2)

assert mongo == TestMongo.objects.get(x=2, y=2)
assert postgres == TestPostgres.objects.get(x=2, y=2)
