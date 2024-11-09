from django.contrib import admin
from .models import Author, Book, Library, Librarian


# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('author',)  # Ensure this is a list or tuple


class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('books',)  # Optional, for ManyToMany fields


class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'library')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Librarian, LibrarianAdmin)
