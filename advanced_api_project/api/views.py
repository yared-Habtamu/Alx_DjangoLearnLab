from django.shortcuts import render
# from rest_framework import generics
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .models import Book, Author
from serializers import BookSerializer
from django.urls import reverse_lazy


class BookListView(ListView):
    model = Book
    fields = ['title', 'publication_year']


class BookDetailView(DetailView):
    model = Book
    template_name = 'api/book_detail.html'
    fields = ['title', 'publication_year']


class BookCreateView(CreateView):
    model = Book
    template_name = 'api/book_list.html'
    fields = ['title', 'publication_year']


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'api/book_form.html'
    fields = ['title', 'publication_year']


class BookDeleteView(DeleteView):
    model = Book
    fields = ['title', 'publication_year']
    success_url = reverse_lazy('book-list')
    template_name = 'api/book_confirm_delete.html'

# Create your views here.
