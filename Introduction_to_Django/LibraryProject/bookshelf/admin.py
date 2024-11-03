from django.contrib import admin
from ,models import Book

# Register your models here.

class BookAdmin(models.Model):
    list_display=('title','author','publication_year')
    list_filter=('title')
    search_fields=('title', 'author')

admin.site.register(Book,BookAdmin)