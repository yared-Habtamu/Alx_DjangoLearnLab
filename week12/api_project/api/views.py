import rest_framework.generics
from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer


# Create your views here.
class BookList(rest_framework.generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
