from django.db import models


# Create your models here.

# class Book(models.Model):
#     objects = None
#     title = models.CharField(max_length=200)
#     author = models.CharField(max_length=100)
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
