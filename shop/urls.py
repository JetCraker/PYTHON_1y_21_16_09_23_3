from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('stuffs/', views.stuff_list, name='stuff_list'),
    path('stuff/<int:pk>', views.stuff_detail, name='stuff_detail'),
    path('add_stuff/', views.add_stuff, name='add_stuff'),

    path('session-demo/', views.session_demo, name='session_demo'),

    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:stuff_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:stuff_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:stuff_id>/', views.update_cart, name='update_cart'),

    path('feedback/', views.send_feedback, name='send_feedback')
]
