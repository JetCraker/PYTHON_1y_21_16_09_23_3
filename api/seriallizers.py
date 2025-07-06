from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'price']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Ціна не може бути від'ємною")
        return value


