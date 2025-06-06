from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('date/', views.current_datetime, name='current_datetime'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]
