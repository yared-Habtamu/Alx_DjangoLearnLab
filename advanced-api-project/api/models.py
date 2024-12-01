from django.db import models
from django.utils import timezone


# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=200)

class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()

    author = models.OneToOneField(Author, on_delete=models.CASCADE)
