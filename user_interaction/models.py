from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField

# Create your models here.


class student(User):
    profile = models.TextField(max_length=2000, blank=True)
    vector_column = SearchVectorField(null=True)

    class Meta:
        indexes = [GinIndex(fields=['vector_column'])]


class employer(User):
    pass


class Job(models.Model):
    title = models.TextField(max_length=200)
    description = models.TextField(max_length=2000)
    mode_of_communication = models.TextField(max_length=200)
    employer = models.ForeignKey(employer, models.CASCADE)
    vector_column = SearchVectorField(null=True)

    class Meta:
        indexes = [GinIndex(fields=['vector_column'])]
