from django.db import models


class Actor(models.Model):
    GENDERS = (('M', 'Male'), ('F', 'Female'))

    name = models.CharField(max_length=50)
    img_url = models.URLField()
    gender = models.CharField(max_length=1, choices=GENDERS)


class Person(models.Model):
    name = models.CharField(max_length=75)
    actor = models.ForeignKey(Actor)
