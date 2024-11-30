from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

        def validate(self, pub_yr):
            if pub_yr > datetime.now().year:
                raise serializers.ValidationError("Not published yet")
            return pub_yr


class AuthorSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=True, read_only=True)

    class Meta(serializers.ModelSerializer):
        model = Author
        fields = ['name','book']