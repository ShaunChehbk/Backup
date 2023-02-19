from django.db import models

# Create your models here.

class Word(models.Model):
    uid = models.PositiveBigIntegerField(primary_key = True)
    word = models.CharField(max_length = 20)
    rating = models.DecimalField(max_digits = 5, decimal_places = 4)
    count = models.SmallIntegerField()

class Interpretation(models.Model):
    uid = models.PositiveBigIntegerField(primary_key = True)
    word = models.ForeignKey(Word, 
        on_delete = models.CASCADE, 
        related_name = 'interpretations',
        related_query_name = 'interpretation')
    interpretation = models.CharField(max_length = 200)

class Example(models.Model):
    uid = models.PositiveBigIntegerField(primary_key = True)
    interpretation = models.ForeignKey(Interpretation, on_delete = models.CASCADE, default = 0)
    example = models.TextField()

class TouchHistory(models.Model):
    uid = models.PositiveBigIntegerField(primary_key = True)
    touchee = models.ForeignKey(Word, 
        on_delete = models.CASCADE,
        related_name = 'touchhistories',
        related_query_name = 'touchhistory')
    # touchee = models.PositiveBigIntegerField(default = 0)
    rate = models.SmallIntegerField(default = 0)