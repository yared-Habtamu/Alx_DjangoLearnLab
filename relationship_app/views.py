from django.shortcuts import render
from .models import Book, Library
from django.views.generic.detail import DetailView

# "relationship_app/list_books.html", "Book.objects.all()"
# Create your views here.
def list_books(request, books=None):
    return render(request, "relationship_app/list_books.html", Book.objects.all() ,{'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
