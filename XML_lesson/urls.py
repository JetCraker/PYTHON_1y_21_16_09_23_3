from django.urls import path
from .views import import_students, student_detail


urlpatterns = [
    path('import_students/', import_students, name='import_students'),
    path('student/<int:pk>/', student_detail, name='student_detail')
]