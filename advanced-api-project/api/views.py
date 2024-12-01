# from django.shortcuts import render
# # from rest_framework import generics
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from .models import Book, Author
# from serializers import BookSerializer
# from django.urls import reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin
#
#
# class BookListView(ListView):
#     model = Book
#     fields = ['title', 'publication_year']
#
#
# class BookDetailView(DetailView):
#     model = Book
#     template_name = 'api/book_detail.html'
#     fields = ['title', 'publication_year']
#
#
# class BookCreateView(LoginRequiredMixin, CreateView):
#     model = Book
#     template_name = 'api/book_list.html'
#     fields = ['title', 'publication_year']
#     login_url = '/login/'
#
#
# class BookUpdateView(LoginRequiredMixin,UpdateView):
#     model = Book
#     template_name = 'api/book_form.html'
#     fields = ['title', 'publication_year']
#     login_url = '/login/'
#
#
#
# class BookDeleteView(DeleteView):
#     model = Book
#     fields = ['title', 'publication_year']
#     success_url = reverse_lazy('book-list')
#     template_name = 'api/book_confirm_delete.html'
#
# # Create your views here.
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from .serializers import BookSerializer
from .models import Book


class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookDeleteView(DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
