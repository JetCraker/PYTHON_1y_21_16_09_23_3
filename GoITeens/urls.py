"""
URL configuration for GoITeens project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('Market/', include('Market.urls')),
    # path('', include('bboard.urls')),
    path('recipes/', include('recipes.urls')),
    path('api/', include('api.urls')),
    path('XML/', include('XML_lesson.urls')),
    path('TEST/', include('TEST.urls')),


    path('', include('shop.urls')),
    path('accounts/', include([
        path('password_reset/',
             auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),
             name='password_reset'),
        path('password_reset/done',
             auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
             name='password_reset_done'),
        path('reset/<uidb64>/<token>',
             auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
             name='password_reset_confirm'),
        path('reset/done',
             auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
             name='password_reset_complete')
    ])),
    path('api/token/', TokenObtainPairView.as_view(), name="token_obtain_part_view"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
