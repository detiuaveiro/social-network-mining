from django.db import models
from djongo import models as mongo_models


# Create your models here.

# Just for testing (remove before merging with master)
class TestMongo(mongo_models.Model):
    x = models.IntegerField()
    y = models.IntegerField()


class TestPostgres(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
