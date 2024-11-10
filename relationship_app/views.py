from django.shortcuts import render
from .models import Book, Library
from django.views.generic.detail import DetailView


# Create your views here.
def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    template_name = 'relationship_app/list_books.html'
    return render(request, template_name, context)


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

