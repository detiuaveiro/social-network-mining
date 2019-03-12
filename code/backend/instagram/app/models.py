from django.db import models


# Create your models here.

class Image(models.Model):
    file = models.FileField()
    total_score = models.IntegerField()
    total_voted = models.IntegerField()

    def __str__(self):
        return self.file.name
