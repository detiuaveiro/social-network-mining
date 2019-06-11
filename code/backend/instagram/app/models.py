from django.db import models


# Create your models here.

class Image(models.Model):
    short_code = models.CharField(primary_key=False, unique=True, max_length=15)
    file = models.FileField()
    total_score = models.IntegerField(default=0)
    total_voted = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.short_code} - {self.file.name}"
