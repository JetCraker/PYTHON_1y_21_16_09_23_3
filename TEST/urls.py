from django.urls import path
from .feeds import StudentsFeed

urlpatterns = [
    path('rss/students/', StudentsFeed(), name='students_rss'),
    # інші шляхи...
]