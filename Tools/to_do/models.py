from pyexpat import model
from django.db import models

# Create your models here.

class Entry(models.Model):
    uid = models.PositiveBigIntegerField(primary_key = True)
    completed = models.BooleanField(default = False)
    complete_time = models.PositiveBigIntegerField(default = 0)
    title = models.CharField(max_length = 200)
    url = models.CharField(max_length = 200)