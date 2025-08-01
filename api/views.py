from rest_framework import viewsets
from .models import Book
from .seriallizers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
