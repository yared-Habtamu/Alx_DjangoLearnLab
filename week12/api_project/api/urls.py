from django.shortcuts import render
from django.urls import path
from .views import BookList

urlpattern = [
    path('books/', BookList.as_view(),name='book-list'),  # Maps to the BookList view
]