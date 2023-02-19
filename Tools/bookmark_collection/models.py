from django.db import models
import uuid

# Create your models here.

class Entry(models.Model):
    # id = models.AutoField()
    uid = models.PositiveIntegerField(primary_key = True)
    hash = models.CharField(max_length = 32)
    title = models.CharField(max_length = 200)
    url = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200)