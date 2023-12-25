from django.db import models

# Create your models here.

class covid(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    carona_status = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    def __str__(self):
        return self.name