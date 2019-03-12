from django.db import models


# Create your models here.

class Image(models.Model):
    file = models.FileField()
    total_score = models.IntegerField(default=0)
    total_voted = models.IntegerField(default=0)

    def __str__(self):
        return self.file.name
